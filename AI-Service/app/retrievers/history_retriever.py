from app.llm.llm_service import LLMService
from app.prompts.history_prompt import HISTORY_PROMPT

import time

from app.utils.logger import logger


class HistoryRetriever:

    def __init__(
        self,
        llm_service: LLMService,
    ):

        self.llm = llm_service.get_llm()

    def invoke(
        self,
        question: str,
        chat_history,
    ):

        prompt = HISTORY_PROMPT.invoke(
            {
                "input": question,
                "chat_history": chat_history,
            }
        )

        start = time.perf_counter()
        
        response = self.llm.invoke(prompt)
        
        elapsed = time.perf_counter() - start
        logger.info("History Retriever took %.3f ms", elapsed*1000)

        logger.info("Chat question rewritten history_messages=%d", len(chat_history))
        logger.info(
            "Standalone question: %s",
            response.content
        )

        return response.content