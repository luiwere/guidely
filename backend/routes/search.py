from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models.record import AnswerResponse, Source
from embeddings import embed_texts
from vector_store import VectorStore
from llm import generate_answer
from logging_utils import track_latency, record_failure

router = APIRouter()
store = VectorStore()


class QueryRequest(BaseModel):
    question: str


@router.post("/query", response_model=AnswerResponse)
async def query(req: QueryRequest):
    if not req.question.strip():
        record_failure("empty_query")
        raise HTTPException(status_code=400, detail="empty query")

    with track_latency("query"):
        try:
            [query_embedding] = embed_texts([req.question])
        except Exception:
            record_failure("embedding_error")
            raise HTTPException(status_code=502, detail="embedding request failed")

        results = store.search(query_embedding, k=3)
        if not results:
            record_failure("no_results")
            raise HTTPException(status_code=404, detail="no results found")

        chunks = [meta for meta, _ in results]
        try:
            answer_text = generate_answer(req.question, chunks)
        except Exception:
            record_failure("llm_timeout")
            raise HTTPException(status_code=502, detail="LLM request timed out or failed")

    sources = [Source(file=c["file"], snippet=c["text"][:200]) for c in chunks]
    return AnswerResponse(answer=answer_text, sources=sources)
