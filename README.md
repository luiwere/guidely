# Guidely

A lightweight internal-docs search assistant. Upload text documents, index them with local
embeddings in FAISS, and ask questions that get answered by an LLM grounded only in the
retrieved chunks — with source snippets attached to every answer.

## Features

- **Local embeddings** via `fastembed` (`BAAI/bge-small-en-v1.5`, 384-dim). No embedding API calls.
- **Vector search** with FAISS `IndexFlatL2`, persisted to disk between restarts.
- **Grounded answers** from any OpenAI-compatible chat endpoint (configured via env), with a
  system prompt that restricts the model to the retrieved context.
- **Incremental indexing** via SHA-256 file hashes, so reindexing skips unchanged documents.
- **Embedding cache** keyed by text hash, avoiding recomputation for unchanged chunks.
- **Observability** — latency (median/p95), cache hit rate, and failure counters exposed on
  `/metrics`; query logs exportable as CSV.

## Stack

| Layer    | Technology                                          |
| -------- | --------------------------------------------------- |
| Backend  | FastAPI, FAISS, fastembed, OpenAI SDK                |
| Frontend | React 18 + Vite                                      |
| Data    | Flat files: FAISS index, JSON hashes, CSV query log  |

## Project layout

```
backend/
  main.py           FastAPI app, CORS, router mounting
  config.py         Env-driven configuration
  routes/           documents, search, metrics, export
  embeddings.py     fastembed wrapper + in-memory cache
  vector_store.py   FAISS index wrapper, metadata persistence
  llm.py            Chat completion client (OpenAI-compatible)
  utils.py          Text extraction and chunking
  hash_utils.py     SHA-256 hashing for change detection
  logging_utils.py  Latency/failure/cache instrumentation
  query_log.py      CSV query logger
  data/
    sample-docs/    Documents to index
    index.faiss     Persisted vector index (generated)
    file_hashes.json
frontend/
  src/pages/        SearchPage, AdminPage
  src/components/   SourceList, UploadForm
  vite.config.js    Dev proxy for /documents, /search, /metrics, /export
```

## Getting started

### 1. Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r ../requirements.txt
cp ../.env.example ../.env                       # then edit .env
uvicorn main:app --reload --port 8000
```

The FastAPI docs are available at http://localhost:8000/docs, and a health check at
`GET /health`.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. Vite proxies `/documents`, `/search`, `/metrics`, and `/export`
to `http://localhost:8000`, so no CORS configuration is needed in development.

## Configuration

All backend settings come from the environment (loaded from `.env` at the repo root via
`python-dotenv`).

| Variable           | Default                        | Description                                        |
| ------------------ | ------------------------------ | -------------------------------------------------- |
| `LLM_API_KEY`      | —                              | API key for the LLM provider. Startup warns if unset. |
| `LLM_BASE_URL`     | `https://api.x.ai/v1`          | Any OpenAI-compatible base URL.                    |
| `LLM_MODEL`        | `grok-4-1-fast`                | Chat model identifier.                             |
| `VECTOR_DB_PATH`   | `./data/index.faiss`           | Path to the persisted FAISS index.                 |

Embedding model and dimension are fixed in `backend/config.py` (`BAAI/bge-small-en-v1.5`, 384).
Changing the model requires deleting `backend/data/index.faiss*` and reindexing.

`.env.example` ships a working Groq configuration; `.env` is gitignored.

## API

| Method | Path                      | Description                                                     |
| ------ | ------------------------- | --------------------------------------------------------------- |
| `GET`  | `/health`                 | Liveness check.                                                  |
| `POST` | `/search/query`           | Ask a question. Returns `{ answer, sources[] }`.                 |
| `POST` | `/documents/upload`       | Upload a `.txt` file. Chunks and embeds it into the index.       |
| `POST` | `/documents/reindex`      | Re-scan the docs folder, indexing only changed files.            |
| `GET`  | `/metrics`                | Latency median/p95, cache hits/misses, failure counts.           |
| `GET`  | `/export/query-logs`      | Download the query log as CSV.                                   |

`POST /search/query`

```bash
curl -X POST http://localhost:8000/search/query \
  -H 'Content-Type: application/json' \
  -d '{"question": "What is the expense reimbursement limit?"}'
```

```json
{
  "answer": "Up to $500 per month, submitted with receipts within 30 days.",
  "sources": [
    { "file": "policy.txt", "snippet": "Reimbursements above $500 require..." }
  ]
}
```

Errors return meaningful status codes: `400` empty query or unsupported file, `404` no
matching documents, `502` embedding or LLM provider failure.

## How retrieval works

1. The question is embedded with the same local model used at index time.
2. FAISS returns the 3 nearest chunks (`IndexFlatL2`, lower distance = closer).
3. Those chunks are concatenated as labelled context and sent to the LLM, which is
   instructed to answer only from that context.
4. Each source file is returned with a 200-character snippet.

Documents are chunked at roughly 800 tokens with 100 tokens of overlap (`utils.chunk_text`
estimates tokens as 4 characters).

## Known gaps

- Only `.txt` files are supported; `extract_text` raises `ValueError` for anything else.
- The `export` router is imported in `main.py` but not mounted, so `/export/query-logs`
  is not currently served.
- `query_log.log_query` exists but is not called by the search route, so the CSV export
  stays empty until that is wired up.
- Metrics are in-process counters; they reset on restart and are not shared across workers.
- Uploads are unauthenticated and CORS allows all origins — add auth and a CORS allowlist
  before deploying anywhere public.

## License

Internal project. No license specified.