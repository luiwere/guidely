from openai import OpenAI

from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = (
    "You are a support assistant. Answer the question using ONLY the provided "
    "context snippets. Be concise. If the context doesn't contain the answer, "
    "say you don't have enough information."
)


def generate_answer(question: str, chunks: list[dict]) -> str:
    context = "\n\n".join(
        f"[Source: {c['file']}]\n{c['text']}" for c in chunks
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
        timeout=10,
    )
    return response.choices[0].message.content
