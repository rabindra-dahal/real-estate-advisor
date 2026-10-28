from typing import List
from app.domain.entities import ChatMessage
from app.interfaces.relational_repo import IRelationalRepository

class GetChatHistoryUseCase:
    def __init__(self, rel_repo: IRelationalRepository):
        self.rel_repo = rel_repo

    async def execute(self, session_id: str, limit: int = 20) -> List[ChatMessage]:
        # Extract chronological chat logs up to the designated processing limit bounds
        return await self.rel_repo.get_session_history(session_id, limit=limit)
