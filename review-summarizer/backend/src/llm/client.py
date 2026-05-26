import logging

from openai import AsyncOpenAI

from src.core.config import get_settings
from src.llm.prompts import SUMMARIZE_REVIEWS_SYSTEM, build_summarization_prompt

logger = logging.getLogger(__name__)


class LLMClient:
    """Асинхронный клиент для взаимодействия с LLM через OpenRouter API."""

    def __init__(self) -> None:
        settings = get_settings()
        self._client = AsyncOpenAI(
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_base_url,
        )
        self._model = settings.llm_model

    async def summarize(self, aggregated: dict) -> str:
        """Генерирует суммаризацию отзывов через LLM.

        Args:
            aggregated: Агрегированные данные анализа тональности.

        Returns:
            Текст суммаризации.
        """
        prompt = build_summarization_prompt(aggregated)

        logger.info("Sending summarization request to LLM (model=%s)", self._model)

        response = await self._client.chat.completions.create(
            model=self._model,
            max_tokens=2048,
            messages=[
                {"role": "system", "content": SUMMARIZE_REVIEWS_SYSTEM},
                {"role": "user", "content": prompt},
            ],
        )

        text = response.choices[0].message.content
        logger.info(
            "LLM response received (tokens: input=%s, output=%s)",
            response.usage.prompt_tokens if response.usage else "?",
            response.usage.completion_tokens if response.usage else "?",
        )
        return text
