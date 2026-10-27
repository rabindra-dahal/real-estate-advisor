from fastapi import APIRouter, HTTPException, Request
from app.delivery.dtos import PropertyRequestDTO, QueryRequestDTO

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
    return use_case.execute(payload.question)
