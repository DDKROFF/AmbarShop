const scheduleCards = document.querySelectorAll('.schedule-card');
const modal = document.querySelector('.auth-modal');
const modalOpenButtons = document.querySelectorAll('[data-open-auth]');
const modalCloseButton = document.querySelector('[data-close-auth]');

const RUSSIAN_MONTHS = [
  'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
  'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
];
const WEEK_DAYS = { 2: 'вторник', 5: 'пятница' };
const DELIVERY_DAYS = [2, 5];

function getNextDeliveryDates(count = 3) {
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const results = [];
  let cursor = new Date(today);

  while (results.length < count) {
    const weekday = cursor.getDay();
    const candidateDay = DELIVERY_DAYS.find((target) => target >= weekday);
    const candidate = new Date(cursor);

    if (candidateDay !== undefined) {
      candidate.setDate(cursor.getDate() + ((candidateDay - weekday + 7) % 7));
    } else {
      candidate.setDate(cursor.getDate() + ((DELIVERY_DAYS[0] + 7) - weekday));
    }

    if (candidate >= today) {
      results.push(candidate);
    }

    cursor = new Date(candidate);
    cursor.setDate(cursor.getDate() + 1);
  }

  return results;
}

function formatDeliveryLabel(date) {
  const dayName = WEEK_DAYS[date.getDay()];
  return `${dayName}, ${date.getDate()} ${RUSSIAN_MONTHS[date.getMonth()]}`;
}

function refreshDeliverySchedule() {
  const upcoming = getNextDeliveryDates(scheduleCards.length);

  scheduleCards.forEach((card, index) => {
    const label = formatDeliveryLabel(upcoming[index]);
    card.dataset.day = label;
    const title = card.querySelector('.card-title');
    if (title) title.textContent = label;
    const statusTag = card.querySelector('.tag');
    if (statusTag) statusTag.textContent = index === 0 ? 'Скоро' : 'Ожидается';
  });

  scheduleCards.forEach((card, index) => {
    card.classList.toggle('active', index === 0);
  });

  const status = document.querySelector('.schedule-status');
  if (status) status.textContent = `Ближайшая: ${scheduleCards[0]?.dataset.day || ''}`;
}

scheduleCards.forEach((card) => {
  card.addEventListener('click', () => {
    scheduleCards.forEach((item) => item.classList.remove('active'));
    card.classList.add('active');
    document.querySelector('.schedule-status')?.replaceChildren(
      document.createTextNode(`Ближайшая: ${card.dataset.day}`)
    );
  });
});

function toggleModal(open) {
  document.body.classList.toggle('modal-open', open);
  modal?.classList.toggle('is-open', open);
}

function toggleReviewModal(open) {
  const reviewModal = document.querySelector('.review-modal');
  if (!reviewModal) return;
  document.body.classList.toggle('modal-open', open);
  reviewModal.classList.toggle('is-open', open);
}

modalOpenButtons.forEach((button) => {
  button.addEventListener('click', (event) => {
    event.preventDefault();
    toggleModal(true);
  });
});

const reviewOpenButtons = document.querySelectorAll('[data-open-review]');
const reviewCloseButton = document.querySelector('[data-close-review]');
const reviewStars = document.querySelectorAll('.review-star');
const reviewRatingInput = document.querySelector('input[name="review-rating"]');

reviewOpenButtons.forEach((button) => {
  button.addEventListener('click', () => toggleReviewModal(true));
});

reviewCloseButton?.addEventListener('click', () => toggleReviewModal(false));

const reviewModal = document.querySelector('.review-modal');
reviewModal?.addEventListener('click', (event) => {
  if (event.target === reviewModal) toggleReviewModal(false);
});

reviewStars.forEach((star) => {
  star.addEventListener('click', () => {
    const value = Number(star.dataset.value);
    if (!reviewRatingInput) return;
    reviewRatingInput.value = value.toString();
    reviewStars.forEach((item) => {
      item.classList.toggle('active', Number(item.dataset.value) <= value);
    });
  });
});

const reviewForm = document.querySelector('.review-form');

reviewForm?.addEventListener('submit', (event) => {
  event.preventDefault();
  toggleReviewModal(false);

  if (reviewForm instanceof HTMLFormElement) {
    reviewForm.reset();
  }

  reviewRatingInput.value = '0';
  reviewStars.forEach((item) => item.classList.remove('active'));
});

const cartToggleButtons = document.querySelectorAll('.cart-toggle');
cartToggleButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const isActive = button.classList.toggle('active');
    button.setAttribute('aria-pressed', String(isActive));
  });
});

function initAccordion() {
  const summaries = document.querySelectorAll('.accordion-summary');
  if (!summaries.length) return;

  summaries.forEach((button) => {
    button.addEventListener('click', () => {
      const item = button.closest('.accordion-item');
      if (!item) return;
      item.classList.toggle('open');
    });
  });
}

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') toggleModal(false);
});

window.addEventListener('layout-ready', initAccordion);
initAccordion();
refreshDeliverySchedule();
