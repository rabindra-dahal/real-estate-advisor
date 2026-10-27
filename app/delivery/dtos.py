from pydantic import BaseModel

class PropertyRequestDTO(BaseModel):
    doc_id: str
    text: str
    price: float
    location: str
    property_type: str

class QueryRequestDTO(BaseModel):
    question: str
