import logging

from fastapi import APIRouter

from app.dependencies.services import chat_service
from app.models.chat_request import ChatRequest

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

@router.post("/")
async def chat(request: ChatRequest):

    return chat_service.chat(
        question=request.question,
        user_id=request.user_id,
        chat_history=request.chat_history,
    )