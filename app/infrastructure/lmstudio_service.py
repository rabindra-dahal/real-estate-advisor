import httpx
from app.interfaces.llm_service import ILLMService

class LMStudioService(ILLMService):
    def __init__(self, base_url: str = "http://localhost:1234/v1"):
        """
        Initializes the dynamic LM Studio adapter.
        Queries the engine runtime status directly to determine model availability.
        """
        self.base_url = base_url
        self.chat_endpoint = f"{self.base_url}/chat/completions"
        self.models_endpoint = f"{self.base_url}/models"

    def _get_active_model_name(self) -> str:
        """
        Fetches the runtime model listing from LM Studio dynamically.
        Falls back to a default label string if no active runtime model is found.
        """
        try:
            response = httpx.get(self.models_endpoint, timeout=5.0)
            response.raise_for_status()
            models_data = response.json()
            
            # Extract the ID of the first model listed in the data array
            if "data" in models_data and len(models_data["data"]) > 0:
                active_model_id = models_data["data"][0]["id"]
                print(f" Dynamic Model Discovery: Detected active model '{active_model_id}'")
                return active_model_id
                
        except (httpx.HTTPError, KeyError, IndexError) as err:
            print(f" Could not auto-detect model from LM Studio: {str(err)}. Falling back to system default.")
        
        # System baseline fallback tag string if the dashboard array is unpopulated
        return "local-model"

    def generate(self, prompt: str) -> str:
        # Dynamically discover what you have running right now in the app window
        active_model = self.get_active_model_name()

        payload = {
            "model": active_model,
            "messages": [
                {"role": "system", "content": "You are a precise, professional Real Estate Advisor. Extract facts accurately."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2  # Low temperature for strict factual real estate data mapping
        }

        try:
            response = httpx.post(self.chat_endpoint, json=payload, timeout=45.0)
            response.raise_for_status()
            
            data = response.json()
            return data["choices"][0]["message"]["content"]
            
        except httpx.HTTPError as http_err:
            raise RuntimeError(f"LM Studio pipeline request failure: {str(http_err)}")
        except (KeyError, IndexError):
            raise RuntimeError("LM Studio returned a malformed chat completion JSON matrix.")
