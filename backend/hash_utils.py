import hashlib
import json
import os

HASH_STORE_PATH = "data/file_hashes.json"


def file_hash(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load_hashes() -> dict:
    if os.path.exists(HASH_STORE_PATH):
        with open(HASH_STORE_PATH, "r") as f:
            return json.load(f)
    return {}


def save_hashes(hashes: dict):
    with open(HASH_STORE_PATH, "w") as f:
        json.dump(hashes, f)


def has_changed(path: str, hashes: dict) -> bool:
    current = file_hash(path)
    return hashes.get(path) != current
