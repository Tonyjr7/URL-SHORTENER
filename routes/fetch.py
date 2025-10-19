from fastapi import APIRouter

from utils.response import Response
from models.urls import get_original_url

router = APIRouter()

@router.get("/fetch{short_code}")
async def fetch_url(short_code: str):
    original_url = get_original_url(short_code)
    if original_url:
        return Response(status_code=200, message="Original URL fetched successfully", data={"original_url": original_url})
    else:
        return Response(status_code=404, message="Short code not found")