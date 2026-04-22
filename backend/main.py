"""
Application entrypoint.

Run with:
    uvicorn main:app --reload
"""

from api.main import app  # noqa: F401
