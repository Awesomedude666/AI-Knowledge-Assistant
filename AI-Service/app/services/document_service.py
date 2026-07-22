import os
import shutil
import time

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config.settings import settings
from app.loaders.pdf_loader import PDFLoader
from app.vectorstore.chroma_service import ChromaService
from app.retrievers.bm25_retriever import BM25RetrieverService

from app.utils.logger import logger


class DocumentService:

    def __init__(
        self,
        pdf_loader: PDFLoader,
        chroma_service: ChromaService,
        bm25_retriever: BM25RetrieverService,
    ):
        self.pdf_loader = pdf_loader
        self.chroma_service = chroma_service
        self.bm25_retriever = bm25_retriever

    def upload_document(
        self,
        file,
        user_id: str,
        document_id: str,
    ):

        started_at = time.monotonic()

        logger.info(
            "Processing document upload user_id=%s document_id=%s filename=%s",
            user_id,
            document_id,
            file.filename,
        )

        user_upload_dir = os.path.join(
            settings.UPLOAD_DIR,
            user_id,
        )

        os.makedirs(
            user_upload_dir,
            exist_ok=True,
        )

        filename = f"{document_id}.pdf"

        file_path = os.path.join(
            user_upload_dir,
            filename,
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        documents = self.pdf_loader.load(file_path)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

        chunks = splitter.split_documents(documents)

        logger.info(
            "Document split user_id=%s document_id=%s chunks=%d",
            user_id,
            document_id,
            len(chunks),
        )

        for index, chunk in enumerate(chunks):
            chunk.metadata["user_id"] = user_id
            chunk.metadata["document_id"] = document_id
            chunk.metadata["chunk_id"] = index
            chunk.metadata["filename"] = file.filename

        self.chroma_service.add_documents(chunks)

        logger.info(
            "Document stored in Chroma user_id=%s document_id=%s",
            user_id,
            document_id,
        )

        self.bm25_retriever.add_documents(
            user_id=user_id,
            documents=chunks,
        )

        logger.info(
            "BM25 updated user_id=%s document_id=%s duration_ms=%d",
            user_id,
            document_id,
            (time.monotonic() - started_at) * 1000,
        )

        # Remove the temporary PDF after successful processing
        if os.path.exists(file_path):
            os.remove(file_path)

        return {
            "document_id": document_id,
            "filename": file.filename,
            "stored_filename": filename,
            "total_chunks": len(chunks),
            "status": "processed",
        }

    def delete_document(
        self,
        document_id: str,
    ):
        self.chroma_service.delete_document(document_id)

        return {
            "message": "Document deleted successfully."
        }