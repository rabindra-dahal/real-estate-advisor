from app.domain.entities import Property
from app.interfaces.relational_repo import IRelationalRepository
from app.interfaces.vector_repo import IVectorRepository

class IngestPropertyUseCase:
    def __init__(self, rel_repo: IRelationalRepository, vec_repo: IVectorRepository):
        self.rel_repo = rel_repo
        self.vec_repo = vec_repo

    async def execute(self, doc_id: str, text: str, price: float, location: str, property_type: str) -> Property:
        if await self.rel_repo.get_property(doc_id):
            raise ValueError("Property structural identity already registered")
            
        property_entity = Property(doc_id, text, price, location, property_type)
        
        # Persist across both adapters safely
        await self.rel_repo.save_property(property_entity)
        self.vec_repo.index_text(
            doc_id=property_entity.doc_id, 
            text=property_entity.text, 
            metadata={"price": price, "location": location, "type": property_type}
        )
        return property_entity
