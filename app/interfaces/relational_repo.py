from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities import Property, AdviceLog, ChatMessage, ErrorLog

class IRelationalRepository(ABC):
    @abstractmethod
    def save_property(self, property_entity: Property) -> None:
        """Persists structural property attributes to the relational database."""
        pass
    
    @abstractmethod
    def get_property(self, doc_id: str) -> Optional[Property]:
        """Retrieves a registered property record by its structural identity string."""
        pass
    
    @abstractmethod
    def save_advice_log(self, log_entity: AdviceLog) -> None:
        """Logs engine selection parameters and metadata tracing details for advisory requests."""
        pass

    @abstractmethod
    def save_message(self, message_entity: ChatMessage) -> None:
        """Appends a dialogue turn into persistent chat messaging schemas."""
        pass

    @abstractmethod
    def get_session_history(self, session_id: str, limit: int = 10) -> List[ChatMessage]:
        """Fetches chronological dialogue history logs belonging to a single workspace thread."""
        pass

    @abstractmethod
    def delete_session_history(self, session_id: str) -> int:
        """Bulk evicts all conversation text turns matching a distinct session identity key."""
        pass

    @abstractmethod
    def save_error_log(self, error_entity: ErrorLog) -> None:
        """Saves system middleware exception tracing records for diagnostic reporting."""
        pass

    @abstractmethod
    def get_recent_errors(self, limit: int = 10) -> List[ErrorLog]:
        """Extracts recent middleware runtime errors sorted chronologically descending."""
        pass

    @abstractmethod
    def get_error_by_id(self, log_id: str) -> Optional[ErrorLog]:
        """Retrieves an explicit system failure trace signature matching a distinct tracking code."""
        pass

    @abstractmethod
    def clear_all_error_logs(self) -> int:
        """Truncates the entire error logging schema. Returns count of records evicted."""
        pass

