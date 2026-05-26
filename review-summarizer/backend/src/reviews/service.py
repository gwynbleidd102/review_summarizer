import asyncio
import logging

from src.nlp.preprocessor import preprocess_batch
from src.nlp.sentiment import analyze_batch
from src.nlp.aggregator import aggregate_sentiments
from src.llm.client import LLMClient
from src.reviews.schemas import (
    ReviewsRequest,
    AnalysisResponse,
    SentimentResult,
    SentimentDistribution,
    SentimentPercentages,
)
from src.reviews.exceptions import NLPProcessingError, LLMSummarizationError

logger = logging.getLogger(__name__)


class ReviewService:
    """Сервис оркестрации NLP-пайплайна: предобработка -> тональность -> агрегация -> LLM."""

    def __init__(self) -> None:
        self._llm_client: LLMClient | None = None

    def _get_llm_client(self) -> LLMClient:
        if self._llm_client is None:
            self._llm_client = LLMClient()
        return self._llm_client

    async def analyze(self, request: ReviewsRequest) -> AnalysisResponse:
        """Полный анализ отзывов: NLP-пайплайн + LLM-суммаризация."""
        raw_texts = [review.text for review in request.reviews]
        logger.info("Starting analysis of %d reviews", len(raw_texts))

        loop = asyncio.get_event_loop()

        try:
            preprocessed = await loop.run_in_executor(
                None, preprocess_batch, raw_texts
            )
        except Exception as exc:
            logger.exception("Preprocessing failed")
            raise NLPProcessingError(f"Ошибка предобработки текста: {exc}") from exc

        try:
            sentiments = await loop.run_in_executor(
                None, analyze_batch, raw_texts
            )
        except Exception as exc:
            logger.exception("Sentiment analysis failed")
            raise NLPProcessingError(f"Ошибка анализа тональности: {exc}") from exc

        aggregated = aggregate_sentiments(raw_texts, sentiments)

        try:
            llm_client = self._get_llm_client()
            summary = await llm_client.summarize(aggregated)
        except Exception as exc:
            logger.exception("LLM summarization failed")
            raise LLMSummarizationError(
                f"Ошибка суммаризации: {exc}"
            ) from exc

        sentiment_results = [
            SentimentResult(text=text, label=str(s["label"]), score=float(s["score"]))
            for text, s in zip(raw_texts, sentiments)
        ]

        return AnalysisResponse(
            total_reviews=aggregated["total_reviews"],
            sentiment_distribution=SentimentDistribution(
                **aggregated["sentiment_distribution"]
            ),
            sentiment_percentages=SentimentPercentages(
                **aggregated["sentiment_percentages"]
            ),
            average_confidence=aggregated["average_confidence"],
            sentiments=sentiment_results,
            summary=summary,
        )
