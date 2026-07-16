from app.embeddings.embedding_service import EmbeddingService
from app.loaders.pdf_loader import PDFLoader
from app.services.document_service import DocumentService
from app.vectorstore.chroma_service import ChromaService


# Create shared dependencies

embedding_service = EmbeddingService()

chroma_service = ChromaService(
    embedding_service=embedding_service,
)

pdf_loader = PDFLoader()


# Create services

document_service = DocumentService(
    pdf_loader=pdf_loader,
    chroma_service=chroma_service,
)