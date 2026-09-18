from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import documents, search

app = FastAPI(title="Guidely")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(search.router, prefix="/search", tags=["search"])


@app.get("/health")
def health():
    return {"status": "ok"}
    
    