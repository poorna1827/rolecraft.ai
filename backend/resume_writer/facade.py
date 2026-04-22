"""
Facade – orchestrates the end-to-end resume rewriting pipeline.

Steps:
    1.  Load & populate prompt templates
    2.  Invoke LLM for structured JSON
    3.  Render DOCX from template
    4.  Post-process (keep-with-next, empty bullets)
    5.  Convert DOCX → PDF
"""

import os
from pathlib import Path

from resume_writer.core.config import settings
from resume_writer.core.logger import logger
from resume_writer.llm.factory import LLMFactory
from resume_writer.models.request import RewriteRequest
from resume_writer.services.pdf_converter import PDFConverter
from resume_writer.services.postprocessor import ResumePostProcessor
from resume_writer.services.renderer import ResumeRenderer


class ResumeEditorManager:
    """High-level entry point consumed by the API layer."""

    def __init__(self, template_path: str | None = None):
        _template = template_path or settings.TEMPLATE_PATH
        self.renderer = ResumeRenderer(template_path=_template)
        self.postprocessor = ResumePostProcessor()
        self.pdf_converter = PDFConverter()

    # ------------------------------------------------------------------ #
    #  Internal helpers
    # ------------------------------------------------------------------ #
    @staticmethod
    def _load_prompt(path: str) -> str:
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return fh.read()
        except FileNotFoundError:
            logger.error("Prompt template missing at: %s", path)
            raise

    @staticmethod
    def _load_resume(resume_name: str) -> str:
        """Loads the base resume text from the configured resumes directory."""
        resume_path = os.path.join(settings.RESUMES_DIR, resume_name)
        try:
            with open(resume_path, "r", encoding="utf-8") as fh:
                return fh.read()
        except FileNotFoundError:
            logger.error("Resume file missing at: %s", resume_path)
            raise FileNotFoundError(f"Resume file '{resume_name}' not found in resumes folder.")

    # ------------------------------------------------------------------ #
    #  Public API
    # ------------------------------------------------------------------ #
    def process(
        self,
        request: RewriteRequest,
        output_dir: str | None = None,
        filename_prefix: str = "Poorna Chander Oruganti",
    ) -> dict:
        out_dir = output_dir or settings.OUTPUT_DIR
        Path(out_dir).mkdir(parents=True, exist_ok=True)

        logger.info("Starting resume edit process using provider: %s", request.provider)

        # 1. Prepare prompts
        system_prompt = self._load_prompt(settings.SYSTEM_PROMPT_PATH)
        user_prompt_template = self._load_prompt(settings.USER_PROMPT_PATH)

        base_resume_text = self._load_resume(request.resume_name)
        
        # Prepend optional metadata to the job description
        jd_context = ""
        if getattr(request, "company_name", None): jd_context += f"Company: {request.company_name}\n"
        if getattr(request, "role", None): jd_context += f"Role: {request.role}\n"
        if getattr(request, "location", None): jd_context += f"Location: {request.location}\n"
        
        full_jd = f"{jd_context}\n{request.job_description}".strip() if jd_context else request.job_description

        user_prompt = user_prompt_template.replace(
            "{{ job_description }}", full_jd
        ).replace("{{ base_resume }}", base_resume_text)
        logger.info("User prompt: %s", user_prompt)

        # 2. LLM generation
        logger.info("Calling LLM Provider…")
        kwargs = {}
        if getattr(request, "model", None) is not None:
            kwargs["model_name"] = request.model
        llm = LLMFactory.get_provider(request.provider, **kwargs)
        resume_data = llm.generate_resume(
            system_prompt=system_prompt, user_prompt=user_prompt
        )

        logger.info("Response: %s", resume_data)

        # 3. Render DOCX
        logger.info("Rendering docx template…")
        if request.template_name:
            template_path = os.path.join(settings.TEMPLATES_DIR, request.template_name)
            logger.info("Using custom template: %s", template_path)
            self.renderer.template_path = template_path

        docx_out = os.path.join(out_dir, f"{filename_prefix}.docx")
        self.renderer.render(resume_data, docx_out)


        # 4. Post-process
        logger.info("Applying post-processing heuristics…")
        self.postprocessor.fix_page_breaks(docx_out)
        self.postprocessor.remove_empty_bullets(docx_out)

        # 5. Convert to PDF
        logger.info("Converting to PDF…")
        pdf_out = os.path.join(out_dir, f"{filename_prefix}.pdf")
        self.pdf_converter.convert_to_pdf(docx_out, pdf_out)

        logger.info("Resume generated successfully at %s", pdf_out)

        return {
            "resume_data": resume_data.model_dump(),
            "docx_path": os.path.abspath(docx_out),
            "pdf_path": os.path.abspath(pdf_out),
        }
