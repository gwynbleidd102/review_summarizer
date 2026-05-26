/**
 * Content script — парсинг DOM отзывов на целевых сайтах.
 * Только извлечение данных, никакой бизнес-логики.
 */

(() => {
  "use strict";

  const AUTO_SCROLL_DELAY_MS = 800;
  const AUTO_SCROLL_MAX_ITERATIONS = 30;

  /**
   * Определяет конфигурацию для текущего сайта по домену.
   */
  function getSiteConfig() {
    const hostname = window.location.hostname;
    for (const [domain, config] of Object.entries(SITE_CONFIGS)) {
      if (hostname.includes(domain)) {
        return config;
      }
    }
    return null;
  }

  /**
   * Находит первый работающий селектор из массива кандидатов.
   */
  function findWorkingSelector(selectors) {
    for (const selector of selectors) {
      const elements = document.querySelectorAll(selector);
      if (elements.length > 0) {
        return { selector, elements };
      }
    }
    return null;
  }

  /**
   * Извлекает текст из элемента по массиву селекторов-кандидатов.
   */
  function extractTextMulti(element, selectors) {
    for (const selector of selectors) {
      const target = element.querySelector(selector);
      if (target) {
        const text = target.textContent.trim().replace(/\s+/g, " ");
        if (text.length > 0) return text;
      }
    }
    return "";
  }

  /**
   * Извлекает текст из элемента по одному селектору.
   */
  function extractText(element, selector) {
    if (!selector) return "";
    const target = element.querySelector(selector);
    if (!target) return "";
    return target.textContent.trim().replace(/\s+/g, " ");
  }

  /**
   * Извлекает рейтинг из элемента.
   */
  function extractRating(element, selector) {
    if (!selector) return null;
    const target = element.querySelector(selector);
    if (!target) return null;

    // Рейтинг через data-атрибут
    const dataRating = target.getAttribute("data-review-rating");
    if (dataRating) {
      return parseFloat(dataRating);
    }

    // Рейтинг через content-атрибут (Яндекс itemprop="ratingValue")
    const content = target.getAttribute("content");
    if (content) {
      const val = parseFloat(content);
      if (!isNaN(val)) return val;
    }

    // Рейтинг через текстовое содержимое (meta-элементы)
    const textVal = parseFloat(target.textContent.trim());
    if (!isNaN(textVal) && textVal >= 1 && textVal <= 5) {
      return textVal;
    }

    // Рейтинг через width в style (процент от 5 звёзд)
    const style = target.getAttribute("style");
    if (style) {
      const widthMatch = style.match(/width:\s*([\d.]+)%/);
      if (widthMatch) {
        return Math.round((parseFloat(widthMatch[1]) / 100) * 5);
      }
    }

    // Рейтинг через aria-label
    const ariaLabel = target.getAttribute("aria-label");
    if (ariaLabel) {
      const ratingMatch = ariaLabel.match(/([\d.]+)/);
      if (ratingMatch) {
        return parseFloat(ratingMatch[1]);
      }
    }

    // Рейтинг через количество закрашенных звёзд (Яндекс)
    const stars = element.querySelectorAll(
      '.business-rating-badge-view__star._full, [class*="star"][class*="active"], [class*="Star"][class*="fill"]'
    );
    if (stars.length > 0) {
      return stars.length;
    }

    return null;
  }

  /**
   * Ожидание указанного времени.
   */
  function delay(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  /**
   * Подсчитывает количество отзывов на странице по конфигурации.
   */
  function countReviews(config) {
    const found = findWorkingSelector(config.reviewSelectors);
    return found ? found.elements.length : 0;
  }

  /**
   * Автоматическая прокрутка контейнера с отзывами для подгрузки всех отзывов.
   *
   * 1. Находит scroll-контейнер по селектору из конфигурации.
   * 2. Прокручивает вниз порциями.
   * 3. После каждой прокрутки ждёт подгрузки новых отзывов.
   * 4. Останавливается, когда новые отзывы перестают появляться.
   * 5. Максимум AUTO_SCROLL_MAX_ITERATIONS итераций (защита от бесконечного скролла).
   */
  async function autoScrollReviews(config) {
    if (!config.scrollContainerSelector) return;

    const scrollContainer = document.querySelector(config.scrollContainerSelector);
    if (!scrollContainer) return;

    let previousCount = countReviews(config);
    let stableIterations = 0;

    for (let i = 0; i < AUTO_SCROLL_MAX_ITERATIONS; i++) {
      scrollContainer.scrollTop = scrollContainer.scrollHeight;
      await delay(AUTO_SCROLL_DELAY_MS);

      const currentCount = countReviews(config);

      if (currentCount === previousCount) {
        stableIterations++;
        if (stableIterations >= 2) {
          break;
        }
      } else {
        stableIterations = 0;
      }

      previousCount = currentCount;
    }
  }

  /**
   * Парсит отзывы со страницы по конфигурации сайта.
   */
  function parseReviewElements(config) {
    const found = findWorkingSelector(config.reviewSelectors);
    if (!found) return [];

    const reviews = [];

    for (const element of found.elements) {
      const text = extractTextMulti(element, config.textSelectors);
      if (!text) continue;

      reviews.push({
        text: text,
        author: extractText(element, config.authorSelector) || null,
        rating: extractRating(element, config.ratingSelector),
      });
    }

    return reviews;
  }

  /**
   * Полный цикл: автоскролл + парсинг отзывов.
   */
  async function collectReviews(config) {
    await autoScrollReviews(config);
    return parseReviewElements(config);
  }

  /**
   * Обработчик сообщений от popup/background.
   */
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "parseReviews") {
      const config = getSiteConfig();

      if (!config) {
        sendResponse({
          success: false,
          error: "Сайт не поддерживается для парсинга отзывов.",
        });
        return true;
      }

      collectReviews(config).then((reviews) => {
        if (reviews.length === 0) {
          sendResponse({
            success: false,
            error:
              "Отзывы не найдены на странице. Откройте карточку заведения и убедитесь, что раздел отзывов загружен.",
          });
          return;
        }

        sendResponse({
          success: true,
          reviews: reviews,
          source: window.location.hostname,
          url: window.location.href,
          count: reviews.length,
        });
      });

      return true;
    }
  });
})();
