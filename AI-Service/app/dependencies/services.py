from app.embeddings.embedding_service import EmbeddingService
from app.loaders.pdf_loader import PDFLoader
from app.services.document_service import DocumentService
from app.vectorstore.chroma_service import ChromaService
from app.llm.llm_service import LLMService
from app.chains.rag_chain import RAGChain
from app.services.chat_service import ChatService
from app.retrievers.retriever_service import RetrieverService
from app.retrievers.bm25_retriever import BM25RetrieverService
from app.retrievers.reranker import RerankerService


# Shared dependencies

embedding_service = EmbeddingService()

chroma_service = ChromaService(
    embedding_service=embedding_service,
)

pdf_loader = PDFLoader()

llm_service = LLMService()

bm25_retriever = BM25RetrieverService()


# Services

document_service = DocumentService(
    pdf_loader=pdf_loader,
    chroma_service=chroma_service,
    bm25_retriever=bm25_retriever,
)

rag_chain = RAGChain(
    llm_service=llm_service,
)

reranker_service = RerankerService()

retriever_service = RetrieverService(
    chroma_service=chroma_service,
    llm_service=llm_service,
    bm25_retriever=bm25_retriever,
    reranker_service=reranker_service
)

chat_service = ChatService(
    retriever_service=retriever_service,
    rag_chain=rag_chain,
)

