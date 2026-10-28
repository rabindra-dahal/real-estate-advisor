import uuid
from app.domain.entities import AdviceLog, ChatMessage
from app.interfaces.relational_repo import IRelationalRepository
from app.interfaces.vector_repo import IVectorRepository
from app.interfaces.llm_service import ILLMService

class QueryAdvisorUseCase:
    def __init__(self, rel_repo: IRelationalRepository, vec_repo: IVectorRepository, primary_llm: ILLMService, fallback_llm: ILLMService, fallback_llm1: ILLMService):
        self.rel_repo = rel_repo
        self.vec_repo = vec_repo
        self.primary_llm = primary_llm
        self.fallback_llm = fallback_llm
        self.fallback_llm1 = fallback_llm1

    async def execute(self, user_query: str, session_id: str) -> dict:
        # 1. Fetch relevant property listings via Semantic Search
        context_docs = self.vec_repo.similarity_search(user_query, limit=3)
        context = "\n\n".join(context_docs) if context_docs else "No property matches found."

        # 2. Reconstruct past chat history milestones from SQLite
        past_messages = await self.rel_repo.get_session_history(session_id, limit=6)
        formatted_history = ""
        for msg in past_messages:
            formatted_history += f"{msg.role.upper()}: {msg.content}\n"

        # 3. Assemble an context-aware prompt layout block
        prompt = f"""You are an expert Real Estate Advisor. Use the following property database listings context to help answer the current conversation thread.

                    Database Property Context:
                    {context}

                    Recent Conversation History:
                    {formatted_history}
                    USER: {user_query}
                    MODEL:
                """

        # 4. Save incoming query statement to persistent message register immediately
        user_message_entity = ChatMessage(str(uuid.uuid4()), session_id, "user", user_query)
        await self.rel_repo.save_message(user_message_entity)
        
        provider = "gemini"
        try:
            answer = await self.primary_llm.generate(prompt)
        except Exception:
            provider = "ollama (fallback)"
            try:
                answer = await self.fallback_llm.generate(prompt)
            except Exception:
                provider = "lmstudio (fallback)"
                try:
                    answer = await self.fallback_llm1.generate(prompt)
                except Exception as e:
                    answer = f"All systems offline: {str(e)}"
                    provider = "none"

        # 5. Save generated answer response output statement to history registers
        model_message_entity = ChatMessage(str(uuid.uuid4()), session_id, "model", answer)
        await self.rel_repo.save_message(model_message_entity)

        # 6. Keep administrative monitoring log trace operational
        log_entity = AdviceLog(str(uuid.uuid4()), user_query, answer, provider)
        await self.rel_repo.save_advice_log(log_entity)

        return {"advice": answer, "engine": provider, "session_id": session_id, "sources": len(context_docs)}
