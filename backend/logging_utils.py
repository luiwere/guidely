import time
import logging
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("guidely")

_latencies = []
_cache_hits = 0
_cache_misses = 0
_failures = {}


@contextmanager
def track_latency(label: str):
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        _latencies.append(elapsed)
        logger.info(f"{label} took {elapsed:.3f}s")


def record_cache(hit: bool):
    global _cache_hits, _cache_misses
    if hit:
        _cache_hits += 1
    else:
        _cache_misses += 1


def record_failure(kind: str):
    _failures[kind] = _failures.get(kind, 0) + 1
    logger.warning(f"failure: {kind} (count={_failures[kind]})")


def get_metrics():
    sorted_lat = sorted(_latencies)
    n = len(sorted_lat)
    median = sorted_lat[n // 2] if n else None
    p95 = sorted_lat[int(n * 0.95) - 1] if n else None
    return {
        "latency_median": median,
        "latency_p95": p95,
        "cache_hits": _cache_hits,
        "cache_misses": _cache_misses,
        "failures": _failures,
    }
