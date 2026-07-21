from langchain_core.messages import AIMessage
from langchain_core.messages import HumanMessage

from app.llm.llm_service import LLMService
from app.retrievers.history_retriever import HistoryRetriever
from app.retrievers.multi_query_retriever import (
    MultiQueryRetrieverService,
)
from app.vectorstore.chroma_service import ChromaService
from app.retrievers.hybrid_retriever import HybridRetriever
from app.retrievers.bm25_retriever import BM25RetrieverService
from app.retrievers.reranker import RerankerService
import time
from app.utils.logger import logger


class RetrieverService:

    def __init__(
        self,
        chroma_service: ChromaService,
        llm_service: LLMService,
        bm25_retriever: BM25RetrieverService,
        reranker_service: RerankerService
    ):

        self.chroma_service = chroma_service
        self.bm25_retriever = bm25_retriever
        self.reranker_service = reranker_service

        self.history_retriever = HistoryRetriever(
            llm_service=llm_service,
        )

        self.multi_query_retriever = MultiQueryRetrieverService(
            llm_service=llm_service,
        )

    def retrieve(
        self,
        question: str,
        user_id: str,
        chat_history,
    ):

        history = self._convert_chat_history(
            chat_history,
        )

        standalone_question = self.history_retriever.invoke(
            question=question,
            chat_history=history,
        )

        # retriever = self.chroma_service.get_retriever(
        #     search_kwargs={
        #         "k": 5,
        #         "filter": {
        #             "user_id": user_id,
        #         },
        #     }
        # )

        hybrid_retriever = HybridRetriever(
            chroma_service=self.chroma_service,
            bm25_retriever=self.bm25_retriever,
            user_id=user_id,
            k=20,
        )
        

        documents = self.multi_query_retriever.invoke(
            question=standalone_question,
            retriever=hybrid_retriever
        )
        
        start = time.perf_counter()
        
        documents = self.reranker_service.get_reranker().compress_documents(
            documents=documents,
            query=standalone_question,
        )
        
        elapsed = time.perf_counter() - start
        logger.info("Reranking took %.3f ms", elapsed*1000)

        return documents

    def _convert_chat_history(
        self,
        chat_history,
    ):

        history = []

        for message in chat_history:

            if message.role == "user":

                history.append(
                    HumanMessage(
                        content=message.content,
                    )
                )

            elif message.role == "assistant":

                history.append(
                    AIMessage(
                        content=message.content,
                    )
                )

        return history