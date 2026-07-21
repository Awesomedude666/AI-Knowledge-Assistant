from app.llm.llm_service import LLMService
from app.prompts.rag_prompt import RAG_PROMPT

from app.utils.logger import logger


class RAGChain:

    def __init__(
        self,
        llm_service: LLMService,
    ):
        self.llm = llm_service.get_llm()

    def invoke(
        self,
        question: str,
        documents,
    ):

        logger.info("Invoking RAG chain documents=%d", len(documents))
        context = "\n\n".join(
            document.page_content
            for document in documents
        )

        prompt = RAG_PROMPT.invoke(
            {
                "context": context,
                "question": question,
            }
        )

        response = self.llm.invoke(prompt)
        logger.info("RAG chain completed")

        return response.content