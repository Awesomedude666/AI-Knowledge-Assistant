

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
    document_id: str = Form(...),
):

    return document_service.upload_document(
        file=file,
        user_id=user_id,
        document_id=document_id,
    )
    
@router.delete("/{user_id}/{document_id}")
async def delete_document(
    user_id: str,
    document_id: str,
):
    return document_service.delete_document(
        user_id=user_id,
        document_id=document_id,
    )