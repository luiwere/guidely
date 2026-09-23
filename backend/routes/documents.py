import os
import shutil
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException

from utils import extract_text, chunk_text
from embeddings import embed_texts
from vector_store import VectorStore
from logging_utils import track_latency, record_failure

router = APIRouter()
UPLOAD_DIR = "data/sample-docs"
store = VectorStore()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        record_failure("missing_filename")
        raise HTTPException(status_code=400, detail="no filename provided")

    dest_path = os.path.join(UPLOAD_DIR, file.filename)
    with track_latency("upload"):
        try:
            with open(dest_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            text = extract_text(dest_path)
        except ValueError as e:
            record_failure("unsupported_file")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception:
            record_failure("corrupted_file")
            raise HTTPException(status_code=500, detail="failed to process file")

        chunks = chunk_text(text)
        if not chunks:
            record_failure("empty_content")
            raise HTTPException(status_code=400, detail="no content extracted from file")

        embeddings = embed_texts(chunks)
        metadata = [
            {"doc_id": str(uuid.uuid4()), "file": file.filename, "text": chunk}
            for chunk in chunks
        ]
        store.add(embeddings, metadata)

    return {"filename": file.filename, "chunks_created": len(chunks)}


@router.post("/reindex")
async def reindex():
    # TODO: walk UPLOAD_DIR, skip files whose content hash is unchanged
    raise HTTPException(status_code=501, detail="not implemented")
