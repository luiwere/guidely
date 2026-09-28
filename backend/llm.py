import logging

from openai import OpenAI

from config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL

logger = logging.getLogger("guidely")

client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)

SYSTEM_PROMPT = (
    "You are a support assistant. Answer the question using ONLY the provided "
    "context snippets. Be concise. If the context doesn't contain the answer, "
    "say you don't have enough information."
)


def generate_answer(question: str, chunks: list[dict]) -> str:
    context = "\n\n".join(
        f"[Source: {c['file']}]\n{c['text']}" for c in chunks
    )
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
            ],
            timeout=15,
        )
    except Exception as e:
        logger.error(f"LLM call failed: {type(e).__name__}: {e}")
        raise
    return response.choices[0].message.content
