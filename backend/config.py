import os
from dotenv import load_dotenv

load_dotenv()

LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.x.ai/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "grok-4-1-fast")

VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./data/index.faiss")
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
EMBEDDING_DIM = 384

if not LLM_API_KEY:
    print("WARNING: LLM_API_KEY is not set")
