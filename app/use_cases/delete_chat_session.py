from app.interfaces.relational_repo import IRelationalRepository

class DeleteChatSessionUseCase:
    def __init__(self, rel_repo: IRelationalRepository):
        self.rel_repo = rel_repo

    def execute(self, session_id: str) -> int:
        # Business logic rule: Verify session exists or enforce eviction permissions if needed
        return self.rel_repo.delete_session_history(session_id)
