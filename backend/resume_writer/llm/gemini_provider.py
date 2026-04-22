from resume_writer.llm.base import LLMProvider
from resume_writer.llm.registry import LLMProviderRegistry
from resume_writer.models.resume import ResumeData
from resume_writer.core.config import settings
from google import genai
from google.genai import types
from resume_writer.core.logger import logger


@LLMProviderRegistry.register("gemini")
class GeminiProvider(LLMProvider):
    def __init__(self, model_name: str = "gemini-3.1-pro-preview"):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_name = model_name

    def generate_resume(self, system_prompt: str, user_prompt: str) -> ResumeData:
        logger.info("Model used:%s", self.model_name)
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[system_prompt, user_prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.3,
            ),
        )
        return ResumeData.model_validate_json(response.text)
