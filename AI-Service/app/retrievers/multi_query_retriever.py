from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.retrievers import BaseRetriever
from app.llm.llm_service import LLMService

from app.retrievers.rrf import reciprocal_rank_fusion

import time

from app.utils.logger import logger


class MultiQueryRetrieverService:

    def __init__(self, llm_service: LLMService):

        self.chain = (
            ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """
You are an AI assistant.

Generate 4 different search queries that help retrieve relevant documents.

Rules:
- Preserve the original meaning.
- Use different wording.
- Cover different aspects if possible.
- Return ONLY the queries.
- One query per line.
""",
                    ),
                    ("human", "{question}"),
                ]
            )
            | llm_service.get_llm()
            | StrOutputParser()
        )

    def generate_queries(
        self,
        question: str,
    ) -> list[str]:

        start = time.perf_counter()

        response = self.chain.invoke(
            {"question": question}
        )
        
        elapsed = time.perf_counter() - start
        logger.info("Multi Query Generation took %.3f ms", elapsed*1000)

        queries = [
            query.strip()
            for query in response.split("\n")
            if query.strip()
        ]

        # Ensure the original query is always searched.
        if question not in queries:
            queries.insert(0, question)

        # Original + 4 generated queries.
        return queries[:5]

    def invoke(
        self,
        question: str,
        retriever: BaseRetriever,
    ) -> list[Document]:

        queries = self.generate_queries(question)

        logger.info("Generated retrieval queries count=%d", len(queries))
        for i, query in enumerate(queries, start=1):
            logger.info("Query %d: %s", i, query)
            
        start = time.perf_counter()

        ranked_lists: list[list[Document]] = []

        for query in queries:

            retrieved_documents = retriever.invoke(query)

            ranked_lists.append(
                retrieved_documents
            )
            
        elapsed = time.perf_counter() - start
        logger.info("Multi Query Retrieval took %.3f ms", elapsed*1000)
        
        start = time.perf_counter()

        fused_documents = reciprocal_rank_fusion(
            ranked_lists=ranked_lists,
        )
        
        elapsed = time.perf_counter() - start
        logger.info("Global RRF took %.3f ms", elapsed*1000)

        return fused_documents[:20]