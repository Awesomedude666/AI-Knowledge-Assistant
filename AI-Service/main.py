from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.health import router as health_router
from app.api.upload import router as upload_router
from app.config.settings import settings
from app.dependencies.services import (
    bm25_retriever,
    chroma_service,
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("========== Building BM25 Indexes ==========")

    user_ids = chroma_service.get_all_user_ids()

    for user_id in user_ids:

        documents = chroma_service.get_documents(
            user_id=user_id,
        )

        print(f"User: {user_id}")
        print(f"Chunks: {len(documents)}")


        bm25_retriever.build_index(
            user_id=user_id,
            documents=documents,
        )
    
    print("========== BM25 Ready ==========")

    yield


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(chat_router)