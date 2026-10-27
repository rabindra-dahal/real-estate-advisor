import os
from google import genai
from app.interfaces.llm_service import ILLMService

class GeminiService(ILLMService):
    def generate(self, prompt: str) -> str:
        key = os.getenv("GEMINI_API_KEY")
        if not key: raise ValueError("Missing API key")
        client = genai.Client(api_key=key)
        return client.models.generate_content(model='gemini-3.5-flash-lite', contents=prompt).text
