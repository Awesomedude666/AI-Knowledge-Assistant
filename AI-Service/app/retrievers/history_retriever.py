from app.llm.llm_service import LLMService
from app.prompts.history_prompt import HISTORY_PROMPT


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

        response = self.llm.invoke(prompt)

        print("=" * 80)
        print("Original Question:")
        print(question)

        print()

        print("Rewritten Question:")
        print(response.content)
        print("=" * 80)

        return response.content