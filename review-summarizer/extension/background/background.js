/**
 * Service worker (background) — HTTP-запросы к бэкенду.
 * Только сетевое взаимодействие, никакой бизнес-логики и DOM-работы.
 */

const API_BASE_URL = "http://localhost:8000/api/v1";

/**
 * Отправляет отзывы на бэкенд для анализа.
 */
async function sendToBackend(reviews, source) {
  const payload = {
    reviews: reviews.map((r) => ({ text: r.text })),
    source: source || null,
  };

  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(
      errorData.detail || `Ошибка сервера: ${response.status}`
    );
  }

  return response.json();
}

/**
 * Обработчик сообщений от popup.
 */
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "analyzeReviews") {
    sendToBackend(message.reviews, message.source)
      .then((result) => {
        sendResponse({ success: true, data: result });
      })
      .catch((error) => {
        sendResponse({ success: false, error: error.message });
      });

    return true;
  }
});
