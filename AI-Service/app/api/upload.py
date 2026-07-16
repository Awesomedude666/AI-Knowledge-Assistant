from fastapi import APIRouter
from app.services.document_service import Document_Service

router = APIRouter()
document_service = Document_Service()

@router.post("/upload")
async def upload():
    await document_service.upload_document()
    return {"message": "Document uploaded successfully."}