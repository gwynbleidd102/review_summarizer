import logging
from functools import lru_cache

from transformers import pipeline, Pipeline  # type: ignore[import-untyped]

from src.core.config import get_settings

logger = logging.getLogger(__name__)

LABEL_MAP: dict[str, str] = {
    "POSITIVE": "positive",
    "NEGATIVE": "negative",
    "NEUTRAL": "neutral",
}


@lru_cache(maxsize=1)
def get_sentiment_pipeline() -> Pipeline:
    settings = get_settings()
    logger.info("Loading sentiment model: %s", settings.sentiment_model)
    return pipeline(
        "sentiment-analysis",
        model=settings.sentiment_model,
        tokenizer=settings.sentiment_model,
    )


def analyze(text: str) -> dict[str, str | float]:
    """Анализ тональности одного текста.

    Returns:
        {"label": "positive"|"negative"|"neutral", "score": float}
    """
    pipe = get_sentiment_pipeline()
    result = pipe(text, truncation=True, max_length=512)[0]
    label = LABEL_MAP.get(result["label"], result["label"].lower())
    return {"label": label, "score": round(result["score"], 4)}


def analyze_batch(texts: list[str]) -> list[dict[str, str | float]]:
    """Анализ тональности пакета текстов."""
    pipe = get_sentiment_pipeline()
    results = pipe(texts, truncation=True, max_length=512, batch_size=16)
    return [
        {
            "label": LABEL_MAP.get(r["label"], r["label"].lower()),
            "score": round(r["score"], 4),
        }
        for r in results
    ]
