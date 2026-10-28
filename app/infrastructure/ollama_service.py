import os
import ollama
from app.interfaces.llm_service import ILLMService


class OllamaService(ILLMService):
    async def generate(self, prompt: str) -> str:
        # Initialize the asynchronous client
        client = ollama.AsyncClient()
        
        # Await the chat completion asynchronously
        response = await client.chat(
            model="llama3.1", 
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response["message"]["content"]
