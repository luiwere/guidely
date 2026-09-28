import os
import pickle
from typing import List, Tuple

import faiss
import numpy as np

from config import VECTOR_DB_PATH, EMBEDDING_DIM

_metadata_path = VECTOR_DB_PATH + ".meta.pkl"


class VectorStore:
    def __init__(self):
        if os.path.exists(VECTOR_DB_PATH) and os.path.exists(_metadata_path):
            self.index = faiss.read_index(VECTOR_DB_PATH)
            with open(_metadata_path, "rb") as f:
                self.metadata = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(EMBEDDING_DIM)
            self.metadata = []  # list of {doc_id, file, text}

    def add(self, embeddings: List[List[float]], metadata: List[dict]):
        vectors = np.array(embeddings, dtype="float32")
        self.index.add(vectors)
        self.metadata.extend(metadata)
        self._save()

    def search(self, query_embedding: List[float], k: int = 3) -> List[Tuple[dict, float]]:
        vector = np.array([query_embedding], dtype="float32")
        distances, indices = self.index.search(vector, k)
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            results.append((self.metadata[idx], float(dist)))
        return results

    def _save(self):
        faiss.write_index(self.index, VECTOR_DB_PATH)
        with open(_metadata_path, "wb") as f:
            pickle.dump(self.metadata, f)


store = VectorStore()
