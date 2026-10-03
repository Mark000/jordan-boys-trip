(() => {
  // Verdict filter
  const buttons = document.querySelectorAll('.filter button');
  const places = document.querySelectorAll('.place');
  const status = document.getElementById('filter-status');
  buttons.forEach(btn => btn.addEventListener('click', () => {
    const f = btn.dataset.filter;
    buttons.forEach(b => b.setAttribute('aria-pressed', String(b === btn)));
    let shown = 0;
    places.forEach(p => {
      const show = f === 'all' || p.dataset.verdict === f;
      p.hidden = !show;
      if (show) { shown++; p.classList.add('in'); }
    });
    status.textContent = `Showing ${shown} place${shown === 1 ? '' : 's'}`;
  }));

  // Highlight current section in the sticky nav
  const tabs = [...document.querySelectorAll('.nav a.tab')];
  const targets = tabs.map(a => document.querySelector(a.getAttribute('href')));
  const setActive = () => {
    const y = window.scrollY + 90;
    let idx = -1;
    targets.forEach((t, i) => { if (t && t.offsetTop <= y) idx = i; });
    tabs.forEach((a, i) => a.setAttribute('aria-current', String(i === idx)));
  };
  window.addEventListener('scroll', setActive, { passive: true });
  setActive();

  // Gentle reveal (CSS disables it under prefers-reduced-motion)
  const reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(entries => entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    }), { rootMargin: '0px 0px -8% 0px' });
    reveals.forEach(el => io.observe(el));
  } else {
    reveals.forEach(el => el.classList.add('in'));
  }
})();
