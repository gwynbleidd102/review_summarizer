import re
from functools import lru_cache

import spacy
from spacy.language import Language

from src.core.config import get_settings


@lru_cache(maxsize=1)
def get_spacy_model() -> Language:
    settings = get_settings()
    return spacy.load(settings.spacy_model)


def clean_text(text: str) -> str:
    """Очистка текста от лишних символов, нормализация пробелов."""
    text = re.sub(r"http\S+|www\.\S+", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[^\w\s.,!?;:\-()«»\"']+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def lemmatize(text: str) -> list[str]:
    """Лемматизация текста: возвращает список лемм без стоп-слов и пунктуации."""
    nlp = get_spacy_model()
    doc = nlp(text)
    return [
        token.lemma_.lower()
        for token in doc
        if not token.is_stop and not token.is_punct and not token.is_space
    ]


def preprocess(text: str) -> str:
    """Полная предобработка: очистка + лемматизация, результат — строка."""
    cleaned = clean_text(text)
    lemmas = lemmatize(cleaned)
    return " ".join(lemmas)


def preprocess_batch(texts: list[str]) -> list[str]:
    """Предобработка списка текстов."""
    return [preprocess(text) for text in texts]
