from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models.record import AnswerResponse

router = APIRouter()


class QueryRequest(BaseModel):
    question: str


@router.post("/query", response_model=AnswerResponse)
async def query(req: QueryRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="empty query")
    # TODO: embed question, retrieve top-k chunks via vector similarity, call LLM
    raise HTTPException(status_code=501, detail="not implemented")
