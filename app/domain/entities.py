from datetime import datetime
from typing import Optional

class Property:
    def __init__(self, doc_id: str, text: str, price: float, location: str, property_type: str, created_at: Optional[datetime] = None):
        self.doc_id = doc_id
        self.text = text
        self.price = price
        self.location = location
        self.property_type = property_type
        self.created_at = created_at or datetime.utcnow()

class AdviceLog:
    def __init__(self, log_id: str, question: str, answer: str, provider_used: str, timestamp: Optional[datetime] = None):
        self.log_id = log_id
        self.question = question
        self.answer = answer
        self.provider_used = provider_used
        self.timestamp = timestamp or datetime.utcnow()
