from typing import List

from fastembed import TextEmbedding

from config import EMBEDDING_MODEL
from logging_utils import record_cache

_model = None

# in-memory cache: text hash -> embedding, avoids re-embedding unchanged chunks
_cache: dict[int, List[float]] = {}


def _get_model() -> TextEmbedding:
    global _model
    if _model is None:
        _model = TextEmbedding(EMBEDDING_MODEL)  # downloads once, then cached on disk
    return _model


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Embed a list of texts locally, using the cache for anything already seen."""
    results: List[List[float] | None] = [None] * len(texts)
    to_embed = []
    to_embed_idx = []

    for i, text in enumerate(texts):
        key = hash(text)
        if key in _cache:
            results[i] = _cache[key]
            record_cache(hit=True)
        else:
            to_embed.append(text)
            to_embed_idx.append(i)
            record_cache(hit=False)

    if to_embed:
        vectors = list(_get_model().embed(to_embed))
        for idx, vec in zip(to_embed_idx, vectors):
            emb = vec.tolist()
            _cache[hash(texts[idx])] = emb
            results[idx] = emb

    return results  # type: ignore
