import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import get_settings
from src.core.exceptions import register_exception_handlers
from src.reviews.router import router as reviews_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    logger.info("Starting application")
    yield
    logger.info("Shutting down application")


def create_app() -> FastAPI:
    settings = get_settings()

    application = FastAPI(
        title="Review Summarizer API",
        description="API для суммаризации пользовательских отзывов с NLP-анализом",
        version="1.0.0",
        lifespan=lifespan,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=[
            f"http://{settings.backend_host}:{settings.backend_port}",
            "chrome-extension://*",
        ],
        allow_origin_regex=r"^chrome-extension://.*$",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(application)
    application.include_router(reviews_router, prefix="/api/v1")

    return application


app = create_app()
