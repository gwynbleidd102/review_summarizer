import pytest

from src.nlp.sentiment import analyze, analyze_batch


class TestAnalyze:
    def test_returns_label_and_score(self) -> None:
        result = analyze("Отличный товар, очень доволен покупкой!")
        assert "label" in result
        assert "score" in result
        assert result["label"] in ("positive", "negative", "neutral")
        assert 0.0 <= result["score"] <= 1.0

    def test_positive_review(self) -> None:
        result = analyze("Замечательный товар! Всё идеально, рекомендую!")
        assert result["label"] == "positive"

    def test_negative_review(self) -> None:
        result = analyze("Ужасное качество, деньги на ветер, никому не советую")
        assert result["label"] == "negative"


class TestAnalyzeBatch:
    def test_batch_returns_list(self) -> None:
        texts = [
            "Отличный товар!",
            "Ужасное качество",
            "Нормально, ничего особенного",
        ]
        results = analyze_batch(texts)
        assert len(results) == 3
        assert all("label" in r and "score" in r for r in results)

    def test_batch_labels_are_valid(self) -> None:
        texts = ["Хорошо", "Плохо"]
        results = analyze_batch(texts)
        for r in results:
            assert r["label"] in ("positive", "negative", "neutral")
            assert 0.0 <= r["score"] <= 1.0
