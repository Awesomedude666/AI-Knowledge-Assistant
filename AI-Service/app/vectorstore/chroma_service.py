from langchain_chroma import Chroma

from app.config.settings import settings
from app.embeddings.embedding_service import EmbeddingService


class ChromaService:
    """
    Responsible for all interactions with the Chroma vector database.
    """

    def __init__(self, embedding_service: EmbeddingService):

        self.vector_store = Chroma(
            persist_directory=settings.CHROMA_DB_PATH,
            embedding_function=embedding_service.get_embedding_model(),
        )

    def add_documents(self, documents):
        """
        Stores documents in Chroma.
        """
        self.vector_store.add_documents(documents)

    def similarity_search(self, query, k=5, filter=None):
        """
        Performs similarity search.
        """
        return self.vector_store.similarity_search(
            query=query,
            k=k,
            filter=filter,
        )

    def get_retriever(self, search_kwargs=None):
        """
        Returns a LangChain retriever.
        """

        if search_kwargs is None:
            search_kwargs = {"k": 5}

        return self.vector_store.as_retriever(
            search_kwargs=search_kwargs
        )

    def delete_document(self, document_id):
        """
        Deletes all chunks belonging to a document.
        """

        self.vector_store.delete(
            where={
                "document_id": document_id
            }
        )