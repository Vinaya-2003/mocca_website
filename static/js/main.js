// MOCCA — front-end interactions
// 1) mobile nav toggle  2) swatch-strip -> collection scroll  3) subtle reveal on scroll

document.addEventListener('DOMContentLoaded', function () {

  // --- mobile nav ---------------------------------------------------
  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.nav-toggle');
  if (toggle && header) {
    toggle.addEventListener('click', function () {
      var isOpen = header.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
  }

  // --- signature swatch navigation -----------------------------------
  var swatches = document.querySelectorAll('.swatch[data-target]');
  swatches.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var target = document.getElementById(btn.dataset.target);
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        target.classList.add('is-highlighted');
        setTimeout(function () { target.classList.remove('is-highlighted'); }, 900);
      }
    });
  });

  // --- reveal-on-scroll (respects reduced motion) ---------------------
  var prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var revealTargets = document.querySelectorAll('.collection-row, .store-card, .product-card, .gallery-figure, .lookbook-figure, .gateway-panel');

  if (!prefersReduced && 'IntersectionObserver' in window) {
    revealTargets.forEach(function (el) { el.style.opacity = 0; el.style.transform = 'translateY(16px)'; el.style.transition = 'opacity 0.6s ease, transform 0.6s ease'; });

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.style.opacity = 1;
          entry.target.style.transform = 'translateY(0)';
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });

    revealTargets.forEach(function (el) { observer.observe(el); });
  }
});
