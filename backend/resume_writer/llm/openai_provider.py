from resume_writer.llm.base import LLMProvider
from resume_writer.llm.registry import LLMProviderRegistry
from resume_writer.models.resume import ResumeData
from resume_writer.core.config import settings
from openai import OpenAI
import json


@LLMProviderRegistry.register("openai")
class OpenAIProvider(LLMProvider):
    def __init__(self, model_name: str = "gpt-4o"):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model_name = model_name

    def generate_resume(self, system_prompt: str, user_prompt: str) -> ResumeData:
        response = self.client.beta.chat.completions.parse(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        data = json.loads(content)

        return ResumeData(**data)   