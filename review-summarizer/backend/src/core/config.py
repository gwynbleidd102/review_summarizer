from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    llm_model: str = "deepseek/deepseek-v4-flash:free"

    sentiment_model: str = "blanchefort/rubert-base-cased-sentiment"
    spacy_model: str = "ru_core_news_sm"

    backend_host: str = "localhost"
    backend_port: int = 8000

    log_level: str = "INFO"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
