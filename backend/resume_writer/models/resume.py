from pydantic import BaseModel, Field
from typing import Dict

class ResumeData(BaseModel):
    summary: str = Field(description="A brief, impactful summary tailored to the job description.")
    exp: Dict[str, Dict[str, str]] = Field(description="Employment history mapping company abbreviations to dictionary of bullet points (b1, b2, etc).")
    proj: Dict[str, Dict[str, str]] = Field(description="Project highlights mapping project abbreviations to dictionary of bullet points (b1, b2, etc).")
    skills: Dict[str, str] = Field(description="Key skills categorized by type (e.g. programming, tools, cloud).")
