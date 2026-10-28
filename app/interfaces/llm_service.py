from abc import ABC, abstractmethod

class ILLMService(ABC):
    @abstractmethod
    async def generate(self, prompt: str) -> str: pass
