from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.config.settings import settings


class EmbeddingService:
    """
    Responsible for creating and managing the embedding model.
    """

    def __init__(self):
        self.embedding_model = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=settings.GOOGLE_API_KEY,
        )

    def get_embedding_model(self):
        """
        Returns the embedding model instance.
        """
        return self.embedding_model