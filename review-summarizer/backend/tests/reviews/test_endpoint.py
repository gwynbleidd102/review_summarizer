import pytest


class TestAnalyzeEndpointValidation:
    """Тесты валидации входных данных endpoint'а /api/v1/analyze."""

    def test_empty_body_returns_422(self, client) -> None:
        response = client.post("/api/v1/analyze", json={})
        assert response.status_code == 422

    def test_empty_reviews_list_returns_422(self, client) -> None:
        response = client.post("/api/v1/analyze", json={"reviews": []})
        assert response.status_code == 422

    def test_review_without_text_returns_422(self, client) -> None:
        response = client.post(
            "/api/v1/analyze", json={"reviews": [{"text": ""}]}
        )
        assert response.status_code == 422

    def test_invalid_json_returns_422(self, client) -> None:
        response = client.post(
            "/api/v1/analyze",
            content=b"not json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 422

    def test_valid_request_accepted(self, client) -> None:
        """Проверяет, что валидный запрос принимается (не 422).

        Полный E2E-тест требует загруженных NLP-моделей и API-ключа,
        поэтому здесь проверяем только, что валидация проходит.
        Ответ может быть 200 или 500/502 в зависимости от окружения.
        """
        response = client.post(
            "/api/v1/analyze",
            json={"reviews": [{"text": "Отличный товар!"}], "source": "test"},
        )
        assert response.status_code != 422
