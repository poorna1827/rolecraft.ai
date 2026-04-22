from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import Optional

# Resolve paths relative to the package root (resume_writer/)
_PACKAGE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # ── LLM API Keys ──────────────────────────────────────────────
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None

    # ── Application ───────────────────────────────────────────────
    LOG_LEVEL: str = "INFO"

    # ── Database ──────────────────────────────────────────────────
    MONGODB_URI: str = "mongodb://localhost:27017" # default
    MONGODB_DB_NAME: str = "resume_db"


    # ── Prompt paths (relative to backend/) ───────────────────────
    SYSTEM_PROMPT_PATH: str = str(_PACKAGE_DIR / "prompts" / "system" / "system_prompt.txt")
    USER_PROMPT_PATH: str = str(_PACKAGE_DIR / "prompts" / "user" / "user_prompt.txt")

    # ── Template paths ────────────────────────────────────────────
    TEMPLATES_DIR: str = str(_PACKAGE_DIR / "templates")
    TEMPLATE_PATH: str = str(_PACKAGE_DIR / "templates" / "resume.docx")


    # ── Output directory for generated files ──────────────────────
    OUTPUT_DIR: str = str(_PACKAGE_DIR / "output")

    # ── Resumes folder (raw candidates) ───────────────────────────
    RESUMES_DIR: str = str(_PACKAGE_DIR.parent / "resumes")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
