from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever

import logging

logger = logging.getLogger(__name__)


class BM25RetrieverService:

    def __init__(self, k:int = 20):
        self.retrievers: dict[str, BM25Retriever] = {}
        self.k = k
        
    def build_index(
        self,
        user_id: str,
        documents: list[Document],
    ):

        logger.info("Building BM25 index user_id=%s documents=%d", user_id, len(documents))
        self.retrievers[user_id] = BM25Retriever.from_documents(
            documents
        )
        self.retrievers[user_id].k = self.k

    def add_documents(
        self,
        user_id: str,
        documents: list[Document],
    ):

        existing = []

        if user_id in self.retrievers:
            existing = self.retrievers[user_id].docs

        logger.info("Updating BM25 index user_id=%s existing=%d added=%d", user_id, len(existing), len(documents))
        self.retrievers[user_id] = BM25Retriever.from_documents(
            existing + documents
        )
        self.retrievers[user_id].k = self.k

    def invoke(
        self,
        user_id: str,
        query: str,
    ):

        retriever = self.retrievers.get(user_id)
        

        if retriever is None:
            logger.info("BM25 index unavailable user_id=%s", user_id)
            return []

        logger.info("BM25 search user_id=%s", user_id)

        return retriever.invoke(query)