from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone

class SaveApplicationRequest(BaseModel):
    job_description: str = Field(..., description="The pasted target Job Description text.")
    provider: str = Field(..., description="The LLM provider used (e.g., openai).")
    model: str = Field(..., description="The specific model used.")
    resume_name: str = Field(..., description="The base resume used.")
    template_name: Optional[str] = Field(None, description="The template file used.")
    company_name: Optional[str] = Field(None, description="The targeted company name.")
    location: Optional[str] = Field(None, description="The targeted location.")
    role: Optional[str] = Field(None, description="The targeted job role.")
    pdf_path: str = Field(..., description="The absolute path to the generated PDF on the server.")
    docx_path: str = Field(..., description="The absolute path to the generated DOCX on the server.")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="The date and time the application was saved.")
