from langchain_google_genai import ChatGoogleGenerativeAI

from app.config.settings import settings


class LLMService:
    """
    Responsible for creating the chat model.
    """

    def __init__(self):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0,
        )

    def get_llm(self):
        return self.llm