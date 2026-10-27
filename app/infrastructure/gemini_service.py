import os
from google import genai
import ollama
from app.interfaces.llm_service import ILLMService

class GeminiService(ILLMService):
    def generate(self, prompt: str) -> str:
        key = os.getenv("GEMINI_API_KEY")
        if not key: raise ValueError("Missing API key")
        client = genai.Client(api_key=key)
        return client.models.generate_content(model='gemini-2.5-flash', contents=prompt).text

class OllamaService(ILLMService):
    def generate(self, prompt: str) -> str:
        response = ollama.chat(model="llama3.1", messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"]
