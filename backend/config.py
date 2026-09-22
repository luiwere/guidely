import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./data/index.faiss")
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIM = 1536

if not OPENAI_API_KEY:
    print("WARNING: OPENAI_API_KEY is not set")
