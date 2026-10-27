from abc import ABC, abstractmethod

class ILLMService(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str: pass
