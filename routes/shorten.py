from fastapi import APIRouter
from pydantic import BaseModel

from utils.response import Response
from models.urls import add_url, client as db
from services.code_generator import generate_code
from services.verify_url import is_valid_url

router = APIRouter()

class URLRequest(BaseModel):
    """Request model for URL shortening."""
    original_url: str

@router.post("/shorten")
async def shorten_url(request: URLRequest):
    original_url = request.original_url
    if not is_valid_url(original_url):
        return Response(status_code=400, message="Invalid URL, cannot be shortened")
    
    try:
        short_code = generate_code()
        add_url(original_url, short_code)
        return Response(status_code=200, message="URL shortened successfully", data={"short_link": short_code})
    except Exception as e:
        return Response(status_code=500, message="Error shortening URL", data={"error": str(e)})
