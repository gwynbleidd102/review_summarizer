from pydantic import BaseModel, Field


class ReviewItem(BaseModel):
    text: str = Field(..., min_length=1, description="Текст отзыва")


class ReviewsRequest(BaseModel):
    reviews: list[ReviewItem] = Field(
        ..., min_length=1, description="Список отзывов для анализа"
    )
    source: str | None = Field(
        default=None, description="Источник отзывов (например, google.com)"
    )


class SentimentResult(BaseModel):
    text: str = Field(..., description="Исходный текст отзыва")
    label: str = Field(..., description="Тональность: positive/negative/neutral")
    score: float = Field(..., description="Уверенность модели")


class SentimentDistribution(BaseModel):
    positive: int = 0
    negative: int = 0
    neutral: int = 0


class SentimentPercentages(BaseModel):
    positive: float = 0.0
    negative: float = 0.0
    neutral: float = 0.0


class AnalysisResponse(BaseModel):
    total_reviews: int = Field(..., description="Общее количество отзывов")
    sentiment_distribution: SentimentDistribution
    sentiment_percentages: SentimentPercentages
    average_confidence: float
    sentiments: list[SentimentResult]
    summary: str = Field(..., description="LLM-суммаризация отзывов")
