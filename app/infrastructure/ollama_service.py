import os
import ollama
from app.interfaces.llm_service import ILLMService


class OllamaService(ILLMService):
    def generate(self, prompt: str) -> str:
        response = ollama.chat(model="llama3.1", messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"]
