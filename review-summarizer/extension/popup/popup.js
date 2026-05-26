/**
 * Popup script — UI-логика и отображение результатов.
 * Только взаимодействие с DOM popup'а и коммуникация через chrome.runtime.
 */

(() => {
  "use strict";

  const analyzeBtn = document.getElementById("analyzeBtn");
  const statusEl = document.getElementById("status");
  const resultsEl = document.getElementById("results");
  const positiveCountEl = document.getElementById("positiveCount");
  const negativeCountEl = document.getElementById("negativeCount");
  const neutralCountEl = document.getElementById("neutralCount");
  const summaryTextEl = document.getElementById("summaryText");

  /**
   * Отображает статус с заданным типом (info, error, success).
   */
  function showStatus(message, type) {
    statusEl.textContent = message;
    statusEl.className = `status ${type}`;
  }

  /**
   * Устанавливает состояние загрузки на кнопке.
   */
  function setLoading(loading) {
    analyzeBtn.disabled = loading;
    if (loading) {
      analyzeBtn.innerHTML =
        '<span class="loader"></span>Анализ...';
    } else {
      analyzeBtn.textContent = "Собрать и проанализировать отзывы";
    }
  }

  /**
   * Отображает результаты анализа.
   */
  function displayResults(data) {
    const dist = data.sentiment_distribution;
    positiveCountEl.textContent = dist.positive;
    negativeCountEl.textContent = dist.negative;
    neutralCountEl.textContent = dist.neutral;
    summaryTextEl.textContent = data.summary;
    resultsEl.classList.add("visible");
  }

  /**
   * Основной обработчик: сбор отзывов -> отправка на бэкенд -> отображение.
   */
  async function handleAnalyze() {
    setLoading(true);
    resultsEl.classList.remove("visible");
    showStatus("Загрузка отзывов (автоскролл страницы)...", "info");

    try {
      const [tab] = await chrome.tabs.query({
        active: true,
        currentWindow: true,
      });

      if (!tab?.id) {
        showStatus("Не удалось определить активную вкладку.", "error");
        setLoading(false);
        return;
      }

      const parseResponse = await chrome.tabs.sendMessage(tab.id, {
        action: "parseReviews",
      });

      if (!parseResponse?.success) {
        showStatus(
          parseResponse?.error || "Ошибка при сборе отзывов.",
          "error"
        );
        setLoading(false);
        return;
      }

      showStatus(
        `Найдено ${parseResponse.count} отзывов. Анализ...`,
        "info"
      );

      const analyzeResponse = await chrome.runtime.sendMessage({
        action: "analyzeReviews",
        reviews: parseResponse.reviews,
        source: parseResponse.source,
      });

      if (!analyzeResponse?.success) {
        showStatus(
          analyzeResponse?.error || "Ошибка при анализе отзывов.",
          "error"
        );
        setLoading(false);
        return;
      }

      showStatus(
        `Анализ завершён: ${parseResponse.count} отзывов обработано.`,
        "success"
      );
      displayResults(analyzeResponse.data);
    } catch (error) {
      showStatus(`Ошибка: ${error.message}`, "error");
    } finally {
      setLoading(false);
    }
  }

  analyzeBtn.addEventListener("click", handleAnalyze);
})();
