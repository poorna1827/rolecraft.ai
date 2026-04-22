from pydantic import BaseModel, Field
from typing import Literal, Optional

class RewriteRequest(BaseModel):
    job_description: str = Field(..., description="The target Job Description text to tailor the resume for.")
    resume_name: str = Field(..., description="The name of the resume file to load from the 'resumes/' folder (e.g., 'ai_resume.json').")
    provider: Literal["openai", "gemini", "claude"] = Field("gemini", description="The LLM provider to use for generation.")
    model: Optional[str] = Field(None, description="The specific model available from the provider to use")
    company_name: Optional[str] = Field(None, description="The company name to tailor the resume for")
    location: Optional[str] = Field(None, description="The location of the job")
    role: Optional[str] = Field(None, description="The job role title")
    template_name: Optional[str] = Field(None, description="The name of the docx template to use from the 'templates/' folder (e.g., 'resume.docx').")

