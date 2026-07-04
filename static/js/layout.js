async function loadPartial(selector, file) {
  const host = document.querySelector(selector);
  if (!host) return;

  try {
    const response = await fetch(file);
    if (!response.ok) throw new Error(`Не удалось загрузить ${file}`);
    host.innerHTML = await response.text();
  } catch (error) {
    console.warn(error.message);
  }
}

async function initLayout() {
  await Promise.all([
    loadPartial('[data-site-header]', './partials/header.html'),
    loadPartial('[data-site-footer]', './partials/footer.html')
  ]);
  window.dispatchEvent(new Event('layout-ready'));
}

window.addEventListener('DOMContentLoaded', initLayout);
