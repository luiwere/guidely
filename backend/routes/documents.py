import os
import shutil
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException

from utils import extract_text, chunk_text
from embeddings import embed_texts
from vector_store import store
from hash_utils import file_hash, load_hashes, save_hashes, has_changed
from logging_utils import track_latency, record_failure

router = APIRouter()
UPLOAD_DIR = "data/sample-docs"


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

        try:
            embeddings = embed_texts(chunks)
        except Exception:
            record_failure("embedding_error")
            raise HTTPException(status_code=502, detail="embedding request failed")

        metadata = [
            {"doc_id": str(uuid.uuid4()), "file": file.filename, "text": chunk}
            for chunk in chunks
        ]
        store.add(embeddings, metadata)

        hashes = load_hashes()
        hashes[dest_path] = file_hash(dest_path)
        save_hashes(hashes)

    return {"filename": file.filename, "chunks_created": len(chunks)}


@router.post("/reindex")
async def reindex():
    with track_latency("reindex"):
        hashes = load_hashes()
        indexed = []
        skipped = []

        for fname in os.listdir(UPLOAD_DIR):
            path = os.path.join(UPLOAD_DIR, fname)
            if not os.path.isfile(path):
                continue

            if not has_changed(path, hashes):
                skipped.append(fname)
                continue

            try:
                text = extract_text(path)
            except ValueError:
                record_failure("unsupported_file")
                continue

            chunks = chunk_text(text)
            if not chunks:
                continue

            try:
                embeddings = embed_texts(chunks)
            except Exception:
                record_failure("embedding_error")
                raise HTTPException(status_code=502, detail="embedding request failed")

            metadata = [
                {"doc_id": str(uuid.uuid4()), "file": fname, "text": chunk}
                for chunk in chunks
            ]
            store.add(embeddings, metadata)
            hashes[path] = file_hash(path)
            indexed.append(fname)

        save_hashes(hashes)

    return {"indexed": indexed, "skipped": skipped}
    