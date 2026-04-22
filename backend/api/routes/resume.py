"""
Resume rewriting endpoint.
"""

from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_resume_manager
from resume_writer.facade import ResumeEditorManager
from resume_writer.models.request import RewriteRequest

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/rewrite", summary="Rewrite a resume for a target job description")
def rewrite_resume(
    request: RewriteRequest,
    manager: ResumeEditorManager = Depends(get_resume_manager),
):
    """
    Accept a base resume + job description, run the LLM pipeline,
    and return the structured resume data together with file paths.
    """
    try:
        import os
        result = manager.process(request)
        if "pdf_path" in result:
            from urllib.parse import quote
            filename = os.path.basename(result["pdf_path"])
            # Return relative or absolute URL for frontend consumption
            result["pdf_url"] = f"http://localhost:8080/output/{quote(filename)}"
        return result
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {exc}",
        ) from exc
