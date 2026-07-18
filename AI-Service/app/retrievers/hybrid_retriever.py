from typing import Any

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from app.retrievers.bm25_retriever import BM25RetrieverService
from app.vectorstore.chroma_service import ChromaService
from app.retrievers.rrf import reciprocal_rank_fusion

import logging
import time

logger = logging.getLogger(__name__)


class HybridRetriever(BaseRetriever):

    chroma_service: ChromaService
    bm25_retriever: BM25RetrieverService

    user_id: str
    k: int = 20

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: Any = None,
    ) -> list[Document]:

        vector_retriever = self.chroma_service.get_retriever(
            search_kwargs={
                "k": self.k,
                "filter":{
                    "user_id": self.user_id,
                },
            },
        )

        start = time.perf_counter()
        
        vector_documents = vector_retriever.invoke(query)
        
        elapsed = time.perf_counter() - start
        logger.info("Vector search took %.3f ms", elapsed*1000)

        logger.info("Vector search completed user_id=%s documents=%d", self.user_id, len(vector_documents))

        start = time.perf_counter()
        
        bm25_documents = self.bm25_retriever.invoke(
            user_id=self.user_id,
            query=query,
        )
        
        elapsed = time.perf_counter() - start
        logger.info("BM25 search took %.3f ms", elapsed*1000)

        logger.info("BM25 search completed user_id=%s documents=%d", self.user_id, len(bm25_documents))

        start = time.perf_counter()

        documents = reciprocal_rank_fusion(
            [
                vector_documents,
                bm25_documents,
            ]
        )
        
        elapsed = time.perf_counter() - start
        logger.info("Local RRF took %.3f ms", elapsed*1000)

        logger.info("Hybrid retrieval fused user_id=%s documents=%d", self.user_id, len(documents))

        return documents[: self.k]