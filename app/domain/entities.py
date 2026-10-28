from datetime import datetime
from typing import Optional

class ChatMessage:
    def __init__(self, message_id: str, session_id: str, role: str, content: str, timestamp: Optional[datetime] = None):
        self.message_id = message_id
        self.session_id = session_id  # Ties multiple messages into a single thread
        self.role = role              # 'user', 'model', or 'system'
        self.content = content
        self.timestamp = timestamp or datetime.utcnow()

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
