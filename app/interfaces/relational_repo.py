from abc import ABC, abstractmethod
from app.domain.entities import Property, AdviceLog

class IRelationalRepository(ABC):
    @abstractmethod
    def save_property(self, property_entity: Property) -> None: pass
    
    @abstractmethod
    def get_property(self, doc_id: str) -> Property | None: pass
    
    @abstractmethod
    def save_advice_log(self, log_entity: AdviceLog) -> None: pass
