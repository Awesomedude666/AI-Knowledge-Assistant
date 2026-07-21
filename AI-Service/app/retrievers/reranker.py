from langchain_classic.retrievers.document_compressors import (
    CrossEncoderReranker,
)
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

import time

from app.utils.logger import logger


class RerankerService:

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
        top_n: int = 5,
    ):

        logger.info("Initializing reranker model=%s top_n=%d", model_name, top_n)
        model = HuggingFaceCrossEncoder(
            model_name=model_name,
        )

        self.reranker = CrossEncoderReranker(
            model=model,
            top_n=top_n,
        )

    def get_reranker(self) -> CrossEncoderReranker:
        return self.reranker