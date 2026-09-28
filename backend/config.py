import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./data/index.faiss")
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
EMBEDDING_DIM = 384

if not OPENAI_API_KEY:
    print("WARNING: OPENAI_API_KEY is not set")
