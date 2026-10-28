from pydantic import BaseModel
from typing import Optional

class PropertyRequestDTO(BaseModel):
    doc_id: str
    text: str
    price: float
    location: str
    property_type: str

class QueryRequestDTO(BaseModel):
    question: str
    session_id: str  # Mandatory key parameter ensuring target execution path clarity
