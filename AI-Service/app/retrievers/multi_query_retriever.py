from langchain_classic.retrievers.multi_query import MultiQueryRetriever

from app.llm.llm_service import LLMService


class MultiQueryRetrieverService:

    def __init__(
        self,
        llm_service: LLMService,
    ):

        self.llm = llm_service.get_llm()

    def invoke(
        self,
        question: str,
        retriever,
    ):

        multi_query_retriever = MultiQueryRetriever.from_llm(
            retriever=retriever,
            llm=self.llm,
        )

        documents = multi_query_retriever.invoke(
            question,
        )

        return documents