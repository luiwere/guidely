from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models.record import AnswerResponse, Source
from embeddings import embed_texts
from vector_store import VectorStore
from llm import generate_answer

router = APIRouter()
store = VectorStore()


class QueryRequest(BaseModel):
    question: str


@router.post("/query", response_model=AnswerResponse)
async def query(req: QueryRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="empty query")

    try:
        [query_embedding] = embed_texts([req.question])
    except Exception:
        raise HTTPException(status_code=502, detail="embedding request failed")

    results = store.search(query_embedding, k=3)
    if not results:
        raise HTTPException(status_code=404, detail="no results found")

    chunks = [meta for meta, _ in results]
    try:
        answer_text = generate_answer(req.question, chunks)
    except Exception:
        raise HTTPException(status_code=502, detail="LLM request timed out or failed")

    sources = [Source(file=c["file"], snippet=c["text"][:200]) for c in chunks]
    return AnswerResponse(answer=answer_text, sources=sources)
