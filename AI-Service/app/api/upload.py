from fastapi import APIRouter, File, Form, UploadFile

from app.dependencies.services import document_service

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post("/upload")
async def upload_document(
    user_id: str = Form(...),
    file: UploadFile = File(...),
):

    return document_service.upload_document(
        file=file,
        user_id=user_id,
    )