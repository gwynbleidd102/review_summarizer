from src.nlp.preprocessor import clean_text, lemmatize, preprocess, preprocess_batch


class TestCleanText:
    def test_removes_urls(self) -> None:
        text = "Отличный товар https://example.com рекомендую"
        result = clean_text(text)
        assert "https://example.com" not in result
        assert "Отличный товар" in result

    def test_removes_html_tags(self) -> None:
        text = "Хороший <b>товар</b> очень <br> качественный"
        result = clean_text(text)
        assert "<b>" not in result
        assert "<br>" not in result
        assert "Хороший" in result

    def test_normalizes_whitespace(self) -> None:
        text = "Много   пробелов   и    табов"
        result = clean_text(text)
        assert "  " not in result

    def test_strips_result(self) -> None:
        text = "  текст с пробелами  "
        result = clean_text(text)
        assert result == "текст с пробелами"

    def test_empty_string(self) -> None:
        assert clean_text("") == ""


class TestLemmatize:
    def test_basic_lemmatization(self) -> None:
        text = "Красивые платья стоят дорого"
        lemmas = lemmatize(text)
        assert len(lemmas) > 0
        assert all(isinstance(lemma, str) for lemma in lemmas)

    def test_removes_stop_words(self) -> None:
        text = "Это очень хороший и качественный товар"
        lemmas = lemmatize(text)
        # Стоп-слова ("это", "и", "очень") должны быть удалены
        assert "это" not in lemmas

    def test_removes_punctuation(self) -> None:
        text = "Товар хороший, качество отличное!"
        lemmas = lemmatize(text)
        assert "," not in lemmas
        assert "!" not in lemmas


class TestPreprocess:
    def test_full_pipeline(self) -> None:
        text = "Отличные кроссовки! https://example.com Рекомендую всем."
        result = preprocess(text)
        assert isinstance(result, str)
        assert "https://example.com" not in result
        assert len(result) > 0

    def test_returns_string(self) -> None:
        result = preprocess("Хороший товар")
        assert isinstance(result, str)


class TestPreprocessBatch:
    def test_processes_multiple_texts(self) -> None:
        texts = ["Хороший товар", "Плохое качество", "Нормальная доставка"]
        results = preprocess_batch(texts)
        assert len(results) == 3
        assert all(isinstance(r, str) for r in results)
