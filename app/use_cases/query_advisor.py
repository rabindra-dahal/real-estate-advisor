import uuid
from app.domain.entities import AdviceLog
from app.interfaces.relational_repo import IRelationalRepository
from app.interfaces.vector_repo import IVectorRepository
from app.interfaces.llm_service import ILLMService

class QueryAdvisorUseCase:
    def __init__(self, rel_repo: IRelationalRepository, vec_repo: IVectorRepository, primary_llm: ILLMService, fallback_llm: ILLMService):
        self.rel_repo = rel_repo
        self.vec_repo = vec_repo
        self.primary_llm = primary_llm
        self.fallback_llm = fallback_llm

    def execute(self, user_query: str) -> dict:
        context_docs = self.vec_repo.similarity_search(user_query, limit=3)
        context = "\n\n".join(context_docs) if context_docs else "No property matches found."

        prompt = f"Context:\n{context}\n\nQuestion: {user_query}"
        
        provider = "gemini"
        try:
            answer = self.primary_llm.generate(prompt)
        except Exception:
            provider = "ollama (fallback)"
            try:
                answer = self.fallback_llm.generate(prompt)
            except Exception as e:
                answer = f"All systems offline: {str(e)}"
                provider = "none"

        log_entity = AdviceLog(str(uuid.uuid4()), user_query, answer, provider)
        self.rel_repo.save_advice_log(log_entity)

        return {"advice": answer, "engine": provider, "sources": len(context_docs)}
