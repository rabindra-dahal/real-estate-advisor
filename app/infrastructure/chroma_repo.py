import chromadb
from sentence_transformers import SentenceTransformer
from app.interfaces.vector_repo import IVectorRepository
from typing import List, Dict

class ChromaRepository(IVectorRepository):
    def __init__(self, path: str = "./chroma_storage"):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection("real_estate_clean")
        self.embed_model = SentenceTransformer("all-MiniLM-L6-v2")

    def index_text(self, doc_id: str, text: str, metadata: Dict):
        embedding = self.embed_model.encode(text).tolist()
        self.collection.upsert(ids=[doc_id], embeddings=[embedding], documents=[text], metadatas=[metadata])

    def similarity_search(self, query_text: str, limit: int) -> List[str]:
        embedding = self.embed_model.encode(query_text).tolist()
        results = self.collection.query(query_embeddings=[embedding], n_results=limit)
        
        formatted_results = []
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        
        for doc, meta in zip(documents, metadatas):
            # Combine the raw vector text block with the metadata attributes
            enriched_text = f"Price: ${meta.get('price')} | Location: {meta.get('location')} | Details: {doc}"
            formatted_results.append(enriched_text)
            
        return formatted_results

