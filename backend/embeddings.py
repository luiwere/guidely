from typing import List
from openai import OpenAI

from config import OPENAI_API_KEY, EMBEDDING_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

# in-memory cache: text hash -> embedding, avoids re-embedding unchanged chunks
_cache: dict[str, List[float]] = {}


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Embed a list of texts, using the cache for anything already seen."""
    results: List[List[float] | None] = [None] * len(texts)
    to_embed = []
    to_embed_idx = []

    for i, text in enumerate(texts):
        key = hash(text)
        if key in _cache:
            results[i] = _cache[key]
        else:
            to_embed.append(text)
            to_embed_idx.append(i)

    if to_embed:
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=to_embed)
        for idx, item in zip(to_embed_idx, response.data):
            _cache[hash(texts[idx])] = item.embedding
            results[idx] = item.embedding

    return results  # type: ignore
