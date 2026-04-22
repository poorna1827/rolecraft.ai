"""
FastAPI application factory.

Configures CORS, includes all routers, and exposes the ASGI ``app``
object that uvicorn will serve.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importing the llm package triggers provider self-registration
import resume_writer.llm  # noqa: F401

from api.routes.resume import router as resume_router
from fastapi.staticfiles import StaticFiles
import os
from resume_writer.core.config import settings

def create_app() -> FastAPI:
    os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
    app = FastAPI(
        title="Resume Writer API",
        description="Takes a base resume and a target job description, "
        "then generates an optimised resume via LLM.",
        version="1.0.0",
    )

    # ── CORS ──────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # tighten in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Routers ───────────────────────────────────────────────────
    app.include_router(resume_router, prefix="/api/v1")
    from api.routes.applications import router as applications_router
    app.include_router(applications_router, prefix="/api/v1")

    # ── Database Lifecycle ────────────────────────────────────────
    from api.db import connect_to_mongo, close_mongo_connection
    app.on_event("startup")(connect_to_mongo)
    app.on_event("shutdown")(close_mongo_connection)

    # ── Static Files ──────────────────────────────────────────────

    app.mount("/output", StaticFiles(directory=settings.OUTPUT_DIR), name="output")

    # ── Health check ──────────────────────────────────────────────
    @app.get("/health", tags=["Health"])
    def health():
        return {"status": "ok"}

    return app


app = create_app()
