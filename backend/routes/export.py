import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from query_log import LOG_PATH

router = APIRouter()


@router.get("/export/query-logs")
def export_query_logs():
    if not os.path.exists(LOG_PATH):
        raise HTTPException(status_code=404, detail="no query logs yet")
    return FileResponse(LOG_PATH, media_type="text/csv", filename="query_log.csv")
