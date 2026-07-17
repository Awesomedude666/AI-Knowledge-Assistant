import os
import shutil
import uuid

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config.settings import settings
from app.loaders.pdf_loader import PDFLoader
from app.vectorstore.chroma_service import ChromaService
from app.retrievers.bm25_retriever import BM25RetrieverService


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
    ):

        document_id = str(uuid.uuid4())

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
        print(f"Created {len(chunks)} chunks")

        for index, chunk in enumerate(chunks):

            chunk.metadata["user_id"] = user_id

            chunk.metadata["document_id"] = document_id

            chunk.metadata["chunk_id"] = index

            chunk.metadata["filename"] = file.filename

        self.chroma_service.add_documents(chunks)
        print("Stored in Chroma")

        self.bm25_retriever.add_documents(
            user_id=user_id,
            documents=chunks,
        )
        print("Updated BM25")

        return {

            "document_id": document_id,

            "filename": file.filename,

            "stored_filename": filename,

            "total_chunks": len(chunks),

            "status": "processed",
        }