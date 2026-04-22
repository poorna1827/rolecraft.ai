import os
import shutil
import json
import secrets
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from resume_writer.models.application import SaveApplicationRequest
from api.db import get_database

router = APIRouter(prefix="/applications", tags=["Applications"])

# Calculate root directory `c:\Users\buddy\Desktop\resume_edit`
# This file is in backend/api/routes/applications.py
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent

@router.post("/save")
def save_application(request: SaveApplicationRequest, db=Depends(get_database)):
    try:
        # 1. Create Folder Structure
        date_str = datetime.now().strftime("%Y-%m-%d")
        company = request.company_name or "UnknownCompany"
        # Sanitize company name for folder
        company_clean = "".join(c for c in company if c.isalnum() or c in " _-").strip().replace(" ", "_")
        rand_hash = secrets.token_hex(3)
        folder_name = f"{company_clean}_{rand_hash}"
        
        target_dir = ROOT_DIR / "data" / date_str / folder_name
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # 2. Paths
        pdf_src = Path(request.pdf_path)
        docx_src = Path(request.docx_path)
        
        if not pdf_src.exists():
            raise HTTPException(status_code=400, detail=f"PDF file not found at {pdf_src}")
        if not docx_src.exists():
            raise HTTPException(status_code=400, detail=f"DOCX file not found at {docx_src}")
            
        pdf_dest = target_dir / pdf_src.name
        docx_dest = target_dir / docx_src.name
        
        # 3. Copy files
        shutil.copy2(pdf_src, pdf_dest)
        shutil.copy2(docx_src, docx_dest)
        
        # 4. Prepare data for JSON and MongoDB
        app_data = request.model_dump()
        # Convert datetime to ISO format string for JSON
        app_data["created_at"] = app_data["created_at"].isoformat()
        # Update paths to the new stored locations
        app_data["stored_pdf_path"] = str(pdf_dest.absolute())
        app_data["stored_docx_path"] = str(docx_dest.absolute())
        
        # 5. Write metadata.json
        metadata_path = target_dir / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(app_data, f, indent=4)
            
        # 6. Save to MongoDB
        collection = db["applications"]
        result = collection.insert_one(app_data)
        
        # Return success with the MongoDB id and new folder path
        return {
            "status": "success",
            "inserted_id": str(result.inserted_id),
            "folder": str(target_dir.absolute())
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
