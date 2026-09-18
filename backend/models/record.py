from pydantic import BaseModel
from typing import Optional


class Chunk(BaseModel):
    id: str
    doc_id: str
    text: str
    embedding: Optional[list[float]] = None


class Source(BaseModel):
    file: str
    snippet: str


class AnswerResponse(BaseModel):
    answer: str
    sources: list[Source]
    