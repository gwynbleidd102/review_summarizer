# Review Summarizer

Система автоматической суммаризации пользовательских отзывов с использованием NLP и LLM.

**Компоненты:**

- **Python-бэкенд (FastAPI)** — NLP-пайплайн: предобработка текста, анализ тональности, агрегация, суммаризация через LLM
- **Chrome-расширение (Manifest V3)** — сбор отзывов с веб-страниц (Google Maps, Яндекс Карты)

## Структура проекта

```
review-summarizer/
├── backend/                    # Python / FastAPI
│   ├── main.py                 # Точка входа, FastAPI app
│   ├── requirements.txt        # Зависимости Python
│   ├── .env.example            # Пример переменных окружения
│   ├── src/
│   │   ├── core/
│   │   │   ├── config.py       # Настройки (pydantic-settings)
│   │   │   └── exceptions.py   # Глобальные обработчики ошибок
│   │   ├── nlp/
│   │   │   ├── preprocessor.py # Токенизация, лемматизация (spaCy)
│   │   │   ├── sentiment.py    # Анализ тональности (HuggingFace)
│   │   │   └── aggregator.py   # Агрегация результатов
│   │   ├── llm/
│   │   │   ├── client.py       # LLM-клиент (OpenRouter / OpenAI SDK)
│   │   │   └── prompts.py      # Шаблоны промптов
│   │   └── reviews/
│   │       ├── schemas.py      # Pydantic-модели запроса/ответа
│   │       ├── service.py      # Оркестрация NLP-пайплайна
│   │       ├── router.py       # POST /api/v1/analyze
│   │       └── exceptions.py   # Кастомные исключения
│   └── tests/
│       ├── conftest.py
│       ├── nlp/                # Тесты NLP-компонентов
│       └── reviews/            # Тесты API endpoint
├── extension/                  # Chrome Extension (Manifest V3)
│   ├── manifest.json
│   ├── config/sites.js         # CSS-селекторы для целевых сайтов
│   ├── content/content.js      # Парсинг DOM отзывов
│   ├── background/background.js# Service worker, HTTP к бэкенду
│   ├── popup/popup.html        # UI расширения
│   ├── popup/popup.js          # Логика popup
│   └── icons/                  # Иконки расширения
```

## Технологический стек

| Компонент          | Технологии                                                 |
| ------------------ | ---------------------------------------------------------- |
| Бэкенд             | Python 3.11+, FastAPI, Pydantic                            |
| NLP                | spaCy (ru_core_news_sm), HuggingFace Transformers (ruBERT) |
| Модель тональности | `blanchefort/rubert-base-cased-sentiment`                  |
| LLM                | OpenRouter API (Claude, GPT, Gemini и др.)                 |
| Расширение         | JavaScript, Chrome Manifest V3                             |
| Тестирование       | pytest, httpx                                              |

---

## Запуск бэкенда

### 1. Требования

- Python 3.11 или выше
- pip
- Аккаунт на [OpenRouter](https://openrouter.ai/) и API-ключ

### 2. Создание виртуального окружения

```bash
cd review-summarizer/backend
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Загрузка языковой модели spaCy

```bash
python -m spacy download ru_core_news_sm
```

### 5. Настройка переменных окружения

Скопируйте файл `.env.example` в `.env` и заполните:

```bash
cp .env.example .env
```

Откройте `.env` и укажите свой API-ключ:

```env
OPENROUTER_API_KEY=sk-or-v1-ваш-ключ-здесь
LLM_MODEL=anthropic/claude-sonnet-4
```

**Доступные модели OpenRouter (примеры):**

| Модель           | Идентификатор                       |
| ---------------- | ----------------------------------- |
| Claude Sonnet 4  | `anthropic/claude-sonnet-4`         |
| GPT-4o           | `openai/gpt-4o`                     |
| Gemini 2.5 Flash | `google/gemini-2.5-flash`           |
| Llama 3.1 70B    | `meta-llama/llama-3.1-70b-instruct` |

Полный список: https://openrouter.ai/models

### 6. Запуск сервера

```bash
cd review-summarizer/backend
source venv/bin/activate
uvicorn main:app --host localhost --port 8000 --reload
```

Сервер будет доступен по адресу: http://localhost:8000

Документация API (Swagger): http://localhost:8000/docs

### 7. Проверка работоспособности

```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "reviews": [
      {"text": "Отличный товар! Качество превосходное, доставка быстрая."},
      {"text": "Ужасное качество, развалился через неделю."},
      {"text": "Нормальный товар за свои деньги, ничего особенного."}
    ],
    "source": "test"
  }'
```

---

## Запуск тестов

```bash
cd review-summarizer/backend
source venv/bin/activate
python -m pytest tests/ -v
```

> При первом запуске тестов тональности автоматически загружается модель HuggingFace (~700 МБ). Последующие запуски используют кешированную модель.

---

## Установка Chrome-расширения

### 1. Откройте страницу расширений Chrome

Перейдите в браузере по адресу:

```
chrome://extensions/
```

### 2. Включите режим разработчика

Переключатель «Режим разработчика» в правом верхнем углу страницы.

### 3. Загрузите расширение

Нажмите **«Загрузить распакованное расширение»** и выберите папку:

```
review-summarizer/extension/
```

### 4. Использование

1. Убедитесь, что бэкенд запущен (`uvicorn main:app ...`)
2. Откройте карточку заведения на Google Maps или Яндекс Картах
3. Нажмите на иконку расширения Review Summarizer
4. Нажмите кнопку **«Собрать и проанализировать отзывы»**
5. Расширение автоматически прокрутит панель отзывов для подгрузки всех отзывов
6. Дождитесь результата — расширение покажет:
   - Распределение тональности (положительные / отрицательные / нейтральные)
   - Текстовое резюме отзывов от LLM

### Поддерживаемые сайты

| Сайт         | URL                                 |
| ------------ | ----------------------------------- |
| Google Maps  | `google.com/maps`, `google.ru/maps` |
| Яндекс Карты | `yandex.ru/maps`, `yandex.com/maps` |

---

## API Reference

### POST /api/v1/analyze

Анализ и суммаризация отзывов.

**Тело запроса:**

```json
{
  "reviews": [{ "text": "Текст отзыва 1" }, { "text": "Текст отзыва 2" }],
  "source": "google.com"
}
```

**Ответ:**

```json
{
  "total_reviews": 2,
  "sentiment_distribution": {
    "positive": 1,
    "negative": 1,
    "neutral": 0
  },
  "sentiment_percentages": {
    "positive": 50.0,
    "negative": 50.0,
    "neutral": 0.0
  },
  "average_confidence": 0.92,
  "sentiments": [
    { "text": "Текст отзыва 1", "label": "positive", "score": 0.95 },
    { "text": "Текст отзыва 2", "label": "negative", "score": 0.89 }
  ],
  "summary": "Резюме отзывов от LLM..."
}
```

---

## Архитектура NLP-пайплайна

```
Отзывы → Предобработка (spaCy) → Анализ тональности (ruBERT) → Агрегация → Суммаризация (LLM)
```

1. **Предобработка** — очистка текста, удаление URL и HTML, лемматизация через spaCy
2. **Анализ тональности** — классификация каждого отзыва (positive/negative/neutral) через `blanchefort/rubert-base-cased-sentiment`
3. **Агрегация** — подсчёт статистики, группировка по тональности
4. **Суммаризация** — генерация структурированного резюме через LLM (OpenRouter)
