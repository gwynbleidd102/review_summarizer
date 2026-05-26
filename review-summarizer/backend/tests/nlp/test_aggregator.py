from src.nlp.aggregator import aggregate_sentiments


class TestAggregateSentiments:
    def test_empty_input(self) -> None:
        result = aggregate_sentiments([], [])
        assert result["total_reviews"] == 0
        assert result["sentiment_distribution"]["positive"] == 0
        assert result["positive_reviews"] == []

    def test_all_positive(self) -> None:
        reviews = ["Отлично", "Замечательно", "Превосходно"]
        sentiments = [
            {"label": "positive", "score": 0.95},
            {"label": "positive", "score": 0.90},
            {"label": "positive", "score": 0.88},
        ]
        result = aggregate_sentiments(reviews, sentiments)
        assert result["total_reviews"] == 3
        assert result["sentiment_distribution"]["positive"] == 3
        assert result["sentiment_distribution"]["negative"] == 0
        assert result["sentiment_percentages"]["positive"] == 100.0
        assert len(result["positive_reviews"]) == 3
        assert len(result["negative_reviews"]) == 0

    def test_mixed_sentiments(self) -> None:
        reviews = ["Хорошо", "Плохо", "Нормально", "Отлично"]
        sentiments = [
            {"label": "positive", "score": 0.9},
            {"label": "negative", "score": 0.85},
            {"label": "neutral", "score": 0.7},
            {"label": "positive", "score": 0.95},
        ]
        result = aggregate_sentiments(reviews, sentiments)
        assert result["total_reviews"] == 4
        assert result["sentiment_distribution"]["positive"] == 2
        assert result["sentiment_distribution"]["negative"] == 1
        assert result["sentiment_distribution"]["neutral"] == 1
        assert result["sentiment_percentages"]["positive"] == 50.0
        assert result["sentiment_percentages"]["negative"] == 25.0
        assert result["positive_reviews"] == ["Хорошо", "Отлично"]
        assert result["negative_reviews"] == ["Плохо"]
        assert result["neutral_reviews"] == ["Нормально"]

    def test_average_confidence(self) -> None:
        reviews = ["A", "B"]
        sentiments = [
            {"label": "positive", "score": 0.8},
            {"label": "negative", "score": 0.6},
        ]
        result = aggregate_sentiments(reviews, sentiments)
        assert result["average_confidence"] == 0.7
