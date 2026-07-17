from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever


class BM25RetrieverService:

    def __init__(self):
        self.retrievers: dict[str, BM25Retriever] = {}

    def build_index(
        self,
        user_id: str,
        documents: list[Document],
    ):

        self.retrievers[user_id] = BM25Retriever.from_documents(
            documents
        )

    def add_documents(
        self,
        user_id: str,
        documents: list[Document],
    ):

        existing = []

        if user_id in self.retrievers:
            existing = self.retrievers[user_id].docs

        self.retrievers[user_id] = BM25Retriever.from_documents(
            existing + documents
        )

    def invoke(
        self,
        user_id: str,
        query: str,
    ):

        retriever = self.retrievers.get(user_id)

        if retriever is None:
            return []

        return retriever.invoke(query)