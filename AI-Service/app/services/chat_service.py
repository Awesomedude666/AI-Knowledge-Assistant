from app.chains.rag_chain import RAGChain
from app.retrievers.retriever_service import RetrieverService

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

        documents = self.retriever_service.retrieve(
            question=question,
            user_id=user_id,
            chat_history=chat_history,
        )

        answer = self.rag_chain.invoke(
            question=question,
            documents=documents,
        )

        return {
            "answer": answer,
            "documents": documents,
        }