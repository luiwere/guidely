from fastapi import APIRouter

from logging_utils import get_metrics

router = APIRouter()


@router.get("/metrics")
def metrics():
    return get_metrics()
