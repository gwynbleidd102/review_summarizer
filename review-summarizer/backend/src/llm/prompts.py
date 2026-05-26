SUMMARIZE_REVIEWS_SYSTEM = (
    "Ты — аналитик пользовательских отзывов. "
    "Твоя задача — составить структурированное резюме на русском языке "
    "на основе предоставленных отзывов и результатов анализа тональности."
)

SUMMARIZE_REVIEWS_TEMPLATE = """\
Проанализируй следующие отзывы и составь структурированное резюме.

Статистика тональности:
- Всего отзывов: {total_reviews}
- Положительных: {positive_count} ({positive_pct}%)
- Отрицательных: {negative_count} ({negative_pct}%)
- Нейтральных: {neutral_count} ({neutral_pct}%)

Положительные отзывы:
{positive_reviews}

Отрицательные отзывы:
{negative_reviews}

Нейтральные отзывы:
{neutral_reviews}

Составь резюме в следующем формате:
1. Общее впечатление (1-2 предложения)
2. Основные достоинства (список)
3. Основные недостатки (список)
4. Рекомендация (1 предложение)
"""


def build_summarization_prompt(aggregated: dict) -> str:
    """Формирует промпт для суммаризации на основе агрегированных данных."""
    positive_texts = aggregated.get("positive_reviews", [])
    negative_texts = aggregated.get("negative_reviews", [])
    neutral_texts = aggregated.get("neutral_reviews", [])
    percentages = aggregated.get("sentiment_percentages", {})
    distribution = aggregated.get("sentiment_distribution", {})

    return SUMMARIZE_REVIEWS_TEMPLATE.format(
        total_reviews=aggregated.get("total_reviews", 0),
        positive_count=distribution.get("positive", 0),
        positive_pct=percentages.get("positive", 0.0),
        negative_count=distribution.get("negative", 0),
        negative_pct=percentages.get("negative", 0.0),
        neutral_count=distribution.get("neutral", 0),
        neutral_pct=percentages.get("neutral", 0.0),
        positive_reviews=_format_reviews(positive_texts),
        negative_reviews=_format_reviews(negative_texts),
        neutral_reviews=_format_reviews(neutral_texts),
    )


def _format_reviews(reviews: list[str]) -> str:
    if not reviews:
        return "Нет отзывов в данной категории."
    return "\n".join(f"- {review}" for review in reviews)
