import logging

from fastapi import APIRouter

from src.reviews.schemas import ReviewsRequest, AnalysisResponse
from src.reviews.service import ReviewService

logger = logging.getLogger(__name__)

router = APIRouter(tags=["reviews"])

_service = ReviewService()


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    summary="Анализ и суммаризация отзывов",
    description="Принимает список отзывов, выполняет NLP-анализ тональности и генерирует суммаризацию через LLM.",
)
async def analyze_reviews(request: ReviewsRequest) -> AnalysisResponse:
    logger.info(
        "Received analysis request: %d reviews (source=%s)",
        len(request.reviews),
        request.source,
    )
    return await _service.analyze(request)
