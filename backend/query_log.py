import csv
import os
import time

LOG_PATH = "data/query_log.csv"
FIELDS = ["timestamp", "question", "latency_seconds", "sources"]


def log_query(question: str, latency: float, sources: list[str]):
    file_exists = os.path.exists(LOG_PATH)
    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "question": question,
            "latency_seconds": f"{latency:.3f}",
            "sources": "|".join(sources),
        })
