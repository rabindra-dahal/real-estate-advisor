from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Union
from datetime import datetime

class PropertyRequestDTO(BaseModel):
    doc_id: str
    text: str
    price: float
    location: str
    property_type: str

class QueryRequestDTO(BaseModel):
    question: str
    session_id: str  # Mandatory key parameter ensuring target execution path clarity

class ChatMessageResponseDTO(BaseModel):
    message_id: str
    role: str
    content: str
    timestamp: Union[datetime, str]

    model_config = ConfigDict(from_attributes=True)

class ChatHistoryResponseDTO(BaseModel):
    session_id: str
    total_messages: int
    messages: List[ChatMessageResponseDTO]

