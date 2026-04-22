"""
FastAPI dependency providers.

Centralises object creation so route handlers stay thin and testable.
"""

from functools import lru_cache
from resume_writer.facade import ResumeEditorManager


@lru_cache(maxsize=1)
def get_resume_manager() -> ResumeEditorManager:
    """Return a singleton ``ResumeEditorManager`` instance."""
    return ResumeEditorManager()
