import os
from google import genai
from app.interfaces.llm_service import ILLMService

class GeminiService(ILLMService):
    async def generate(self, prompt: str) -> str:
        key = os.getenv("GEMINI_API_KEY")
        if not key: raise ValueError("Missing API key configuration parameters")
        
        # Instantiate the official async-capable client configuration layer
        client = genai.Client(api_key=key)
        response = await client.aio.models.generate_content(
            model='gemini-3.5-flash-lite', # Or your functional verified model choice string
            contents=prompt
        )
        return response.text
