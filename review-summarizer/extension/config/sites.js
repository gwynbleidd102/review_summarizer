/**
 * Конфигурация CSS-селекторов для парсинга отзывов на целевых сайтах.
 *
 * reviewSelectors — массив селекторов-кандидатов для контейнера отзыва (fallback).
 * textSelectors — массив селекторов для текста отзыва внутри контейнера.
 * ratingSelector / authorSelector — опциональные.
 * scrollContainerSelector — селектор контейнера, который нужно прокручивать для подгрузки отзывов.
 */
const SITE_CONFIGS = {
  "google.com": {
    reviewSelectors: [
      '[data-review-id]',
      ".jftiEf",
    ],
    textSelectors: [
      ".MyEned span",
      ".wiI7pd",
    ],
    ratingSelector: '[aria-label*="star"]',
    authorSelector: ".d4r55",
    scrollContainerSelector: 'div.m6QErb.DxyBCb.kA9KIf.dS8AEf',
  },
  "google.ru": {
    reviewSelectors: [
      '[data-review-id]',
      ".jftiEf",
    ],
    textSelectors: [
      ".MyEned span",
      ".wiI7pd",
    ],
    ratingSelector: '[aria-label*="star"]',
    authorSelector: ".d4r55",
    scrollContainerSelector: 'div.m6QErb.DxyBCb.kA9KIf.dS8AEf',
  },
  "yandex.ru": {
    reviewSelectors: [
      ".business-reviews-card-view__review",
      ".business-review-view__info",
    ],
    textSelectors: [
      ".business-review-view__body-text",
      ".spoiler-view__text-container",
    ],
    ratingSelector: '[itemprop="ratingValue"]',
    authorSelector: 'span[itemprop="name"]',
    scrollContainerSelector: ".scroll__container",
  },
  "yandex.com": {
    reviewSelectors: [
      ".business-reviews-card-view__review",
      ".business-review-view__info",
    ],
    textSelectors: [
      ".business-review-view__body-text",
      ".spoiler-view__text-container",
    ],
    ratingSelector: '[itemprop="ratingValue"]',
    authorSelector: 'span[itemprop="name"]',
    scrollContainerSelector: ".scroll__container",
  },
};
