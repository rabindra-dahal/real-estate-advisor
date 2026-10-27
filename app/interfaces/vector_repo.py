from abc import ABC, abstractmethod
from typing import List, Dict

class IVectorRepository(ABC):
    @abstractmethod
    def index_text(self, doc_id: str, text: str, metadata: Dict) -> None: pass
    
    @abstractmethod
    def similarity_search(self, query_text: str, limit: int) -> List[str]: pass
