from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities import Property, AdviceLog, ChatMessage

class IRelationalRepository(ABC):
    @abstractmethod
    def save_property(self, property_entity: Property) -> None: pass
    
    @abstractmethod
    def get_property(self, doc_id: str) -> Optional[Property]: pass
    
    @abstractmethod
    def save_advice_log(self, log_entity: AdviceLog) -> None: pass

    @abstractmethod
    def save_message(self, message_entity: ChatMessage) -> None: pass

    @abstractmethod
    def get_session_history(self, session_id: str, limit: int = 10) -> List[ChatMessage]: pass
