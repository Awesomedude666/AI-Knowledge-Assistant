# app/api/health.py

from fastapi import APIRouter
from app.config.settings import settings

router = APIRouter()


@router.get("/health")
def health():

    return {
        "status": "ok",
        "application": settings.APP_NAME,
        "environment": settings.APP_ENV
    }