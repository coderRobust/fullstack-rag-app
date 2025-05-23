from fastapi import APIRouter, Body, HTTPException
from services.qa_engine import get_answer

router = APIRouter()


@router.post("/")
async def qa_endpoint(payload: dict = Body(...)):
    question = payload.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="Missing question field")
    try:
        answer = await get_answer(question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal error: {str(e)}")
