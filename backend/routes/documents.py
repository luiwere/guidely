import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException

from utils import extract_text, chunk_text

router = APIRouter()
UPLOAD_DIR = "data/sample-docs"


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="no filename provided")

    dest_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(dest_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        text = extract_text(dest_path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="failed to process file")

    chunks = chunk_text(text)
    # TODO: embed chunks, persist to vector DB
    return {"filename": file.filename, "chunks_created": len(chunks)}


@router.post("/reindex")
async def reindex():
    # TODO: re-run embedding pipeline, skip unchanged files
    raise HTTPException(status_code=501, detail="not implemented")
