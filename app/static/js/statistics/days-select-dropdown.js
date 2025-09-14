const btn = document.getElementById('range-btn');
const menu = document.getElementById('range-menu');

function positionMenu() {
  const r = btn.getBoundingClientRect();
  menu.style.left = `${r.left}px`;
  menu.style.top  = `${r.bottom + window.scrollY}px`;
}

function openMenu() {
  positionMenu();
  menu.classList.add('open');
  const first = menu.querySelector('.menu-item');
  if (first) first.focus();
}

function closeMenu() {
  menu.classList.remove('open');
}

btn.addEventListener('click', (e) => {
  e.stopPropagation();
  menu.classList.contains('open') ? closeMenu() : openMenu();
});

document.addEventListener('click', (e) => {
  if (!menu.contains(e.target) && e.target !== btn) closeMenu();
});

document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeMenu(); });

menu.addEventListener('click', (e) => {
  const item = e.target.closest('.menu-item');
  if (item) {
    closeMenu();
  }
});

// document.getElementById('range-send').addEventListener('click', () => {
//   const days = parseInt(document.getElementById('custom-days').value, 10);
//   if (!Number.isNaN(days) && days > 0) {
//     console.log('custom days =', days);
//     closeMenu();
//   }
// });
