from collections import Counter


def aggregate_sentiments(
    reviews: list[str],
    sentiments: list[dict[str, str | float]],
) -> dict:
    """Агрегация результатов анализа тональности.

    Returns:
        {
            "total_reviews": int,
            "sentiment_distribution": {"positive": int, "negative": int, "neutral": int},
            "sentiment_percentages": {"positive": float, ...},
            "average_confidence": float,
            "positive_reviews": [str, ...],
            "negative_reviews": [str, ...],
            "neutral_reviews": [str, ...],
        }
    """
    total = len(reviews)
    if total == 0:
        return {
            "total_reviews": 0,
            "sentiment_distribution": {"positive": 0, "negative": 0, "neutral": 0},
            "sentiment_percentages": {"positive": 0.0, "negative": 0.0, "neutral": 0.0},
            "average_confidence": 0.0,
            "positive_reviews": [],
            "negative_reviews": [],
            "neutral_reviews": [],
        }

    labels = [s["label"] for s in sentiments]
    scores = [s["score"] for s in sentiments]
    distribution = Counter(labels)

    positive_reviews: list[str] = []
    negative_reviews: list[str] = []
    neutral_reviews: list[str] = []

    for review, sentiment in zip(reviews, sentiments):
        label = sentiment["label"]
        if label == "positive":
            positive_reviews.append(review)
        elif label == "negative":
            negative_reviews.append(review)
        else:
            neutral_reviews.append(review)

    return {
        "total_reviews": total,
        "sentiment_distribution": {
            "positive": distribution.get("positive", 0),
            "negative": distribution.get("negative", 0),
            "neutral": distribution.get("neutral", 0),
        },
        "sentiment_percentages": {
            "positive": round(distribution.get("positive", 0) / total * 100, 1),
            "negative": round(distribution.get("negative", 0) / total * 100, 1),
            "neutral": round(distribution.get("neutral", 0) / total * 100, 1),
        },
        "average_confidence": round(sum(scores) / total, 4),
        "positive_reviews": positive_reviews,
        "negative_reviews": negative_reviews,
        "neutral_reviews": neutral_reviews,
    }
