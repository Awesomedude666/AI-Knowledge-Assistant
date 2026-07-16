import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        self.APP_NAME = os.getenv("APP_NAME")
        self.APP_ENV = os.getenv("APP_ENV")

        self.HOST = os.getenv("HOST")
        self.PORT = int(os.getenv("PORT", 8000))

        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

        self.CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH")

        self.UPLOAD_DIR = os.getenv("UPLOAD_DIR")

        self.CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
        self.CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))


settings = Settings()