from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.urls import client as db
from utils.response import Response
from routes.shorten import router as shorten_router
from routes.fetch import router as fetch_router

app = FastAPI(title="URL Shortener Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return Response(status_code=200, message="URL Shortener Service is running")

app.include_router(shorten_router)
app.include_router(fetch_router)

@app.get("/health")
async def health_check():
    try:
        db.admin.command('ping')  # checks MongoDB connection
        return Response(status_code=200, message="Database reachable")
    except Exception:
        return Response(status_code=500, message="Database not reachable")