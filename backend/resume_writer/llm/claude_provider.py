import json
from anthropic import Anthropic
from resume_writer.llm.base import LLMProvider
from resume_writer.llm.registry import LLMProviderRegistry
from resume_writer.models.resume import ResumeData
from resume_writer.core.config import settings
from resume_writer.core.logger import logger


@LLMProviderRegistry.register("claude")
class ClaudeProvider(LLMProvider):
    def __init__(self, model_name: str = "claude-haiku-4-5-20251001"):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model_name = model_name

    def generate_resume(self, system_prompt: str, user_prompt: str) -> ResumeData:
        system_prompt += "\n\nYou must respond ONLY with raw JSON matching the required schema. Do not include markdown formatting or json blocks."
        
        response = self.client.messages.create(
            model=self.model_name,
            max_tokens=4000,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
        )

        # response.content[0].text holds the actual string
        text_response = response.content[0].text
        # In case the model still outputs markdown like ```json ... ```
        if text_response.startswith("```json"):
            text_response = text_response.strip("`").removeprefix("json").strip()
            
        return ResumeData.model_validate_json(text_response)
