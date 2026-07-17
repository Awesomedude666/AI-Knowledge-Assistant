from typing import Any

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from app.retrievers.bm25_retriever import BM25RetrieverService
from app.vectorstore.chroma_service import ChromaService
from app.retrievers.rrf import reciprocal_rank_fusion


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

        vector_documents = vector_retriever.invoke(query)

        print("\n========== Vector Search ==========")
        print(f"Retrieved {len(vector_documents)} documents")

        for doc in vector_documents:
            print(doc.metadata["chunk_id"])

        bm25_documents = self.bm25_retriever.invoke(
            user_id=self.user_id,
            query=query,
        )

        print("\n========== BM25 ==========")
        print(f"Retrieved {len(bm25_documents)} documents")

        for doc in bm25_documents:
            print(doc.metadata["chunk_id"])

        documents = reciprocal_rank_fusion(
            [
                vector_documents,
                bm25_documents,
            ]
        )

        print("\n========== RRF ==========")
        print(f"Retrieved {len(documents)} documents")

        for document in documents:
            print(document.metadata["chunk_id"])

        return documents[: self.k]