from app.chains.rag_chain import RAGChain
from app.retrievers.retriever_service import RetrieverService

import time

from app.utils.logger import logger

# we are importing these classes only for type checking in the chatService.
# chat service takes object of these classes as input in the constructor. So we need to import them for type checking.

class ChatService:

    def __init__(
        self,
        retriever_service: RetrieverService,
        rag_chain: RAGChain,
    ):

        self.retriever_service = retriever_service
        self.rag_chain = rag_chain

    def chat(
        self,
        question: str,
        user_id: str,
        chat_history,
    ):

        start = time.perf_counter()
        logger.info("Retrieving chat context user_id=%s history_messages=%d", user_id, len(chat_history))
        documents = self.retriever_service.retrieve(
            question=question,
            user_id=user_id,
            chat_history=chat_history,
        )

        logger.info("Generating chat answer user_id=%s retrieved_documents=%d", user_id, len(documents))
        
        answer = self.rag_chain.invoke(
            question=question,
            documents=documents,
        )
        
        elapsed = time.perf_counter() - start
        logger.info("Chat service took %.3f ms", elapsed*1000)

        return {
            "answer": answer,
            "documents": documents,
        }