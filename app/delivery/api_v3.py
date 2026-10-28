from fastapi import APIRouter, HTTPException, Request, Query, status
from app.delivery.dtos import PropertyRequestDTO, QueryRequestDTO, ChatHistoryResponseDTO
from app.delivery.dtos import ChatMessageResponseDTO

router = APIRouter(prefix="/api/v3")

@router.post("/properties")
def add_property(payload: PropertyRequestDTO, request: Request):
    use_case = request.app.state.ingest_property_use_case
    try:
        use_case.execute(payload.doc_id, payload.text, payload.price, payload.location, payload.property_type)
        return {"status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/advise")
def get_advice(payload: QueryRequestDTO, request: Request):
    use_case = request.app.state.query_advisor_use_case
    return use_case.execute(payload.question, payload.session_id)

@router.get("/chat/{session_id}/history", response_model=ChatHistoryResponseDTO)
def get_chat_history(session_id: str, request: Request, limit: int = Query(default=20, ge=1, le=100)):
    use_case = request.app.state.get_chat_history_use_case
    try:
        messages_entities = use_case.execute(session_id, limit=limit)
        
        # Serialize pure domain entity attributes straight into DTO configurations
        formatted_messages = [
            ChatMessageResponseDTO(
                message_id=msg.message_id,
                role=msg.role,
                content=msg.content,
                timestamp=msg.timestamp
            ) for msg in messages_entities
        ]
        
        return ChatHistoryResponseDTO(
            session_id=session_id,
            total_messages=len(formatted_messages),
            messages=formatted_messages
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/chat/{session_id}", status_code=status.HTTP_200_OK)
def delete_chat_session(session_id: str, request: Request):
    use_case = request.app.state.delete_chat_session_use_case
    try:
        records_removed = use_case.execute(session_id)
        
        if records_removed == 0:
            return {
                "status": "ignored",
                "message": f"No active message sequences found for target session identity '{session_id}'"
            }
            
        return {
            "status": "success",
            "message": f"Successfully evicted workspace thread '{session_id}' completely from storage matrix.",
            "records_purged": records_removed
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
