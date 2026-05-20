const navToggle = document.getElementById('navToggle');
const pageNav = document.getElementById('pageNav');

navToggle?.addEventListener('click', () => {
  pageNav.classList.toggle('is-open');
});
