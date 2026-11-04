(function () {
  var root = document.documentElement;
  var themeButton = document.getElementById('themeToggle');
  var drawingButton = document.getElementById('drawingToggle');
  var systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
  var savedTheme;
  try { savedTheme = localStorage.getItem('swiss-theme'); } catch (e) {}
  function setTheme(theme) {
    root.dataset.theme = theme;
    themeButton.setAttribute('aria-pressed', String(theme === 'dark'));
    themeButton.setAttribute('aria-label', theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
  }
  setTheme(savedTheme === 'dark' || savedTheme === 'light' ? savedTheme : systemTheme.matches ? 'dark' : 'light');
  themeButton.addEventListener('click', function () {
    savedTheme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    setTheme(savedTheme);
    try { localStorage.setItem('swiss-theme', savedTheme); } catch (e) {}
  });
  systemTheme.addEventListener('change', function (event) {
    if (!savedTheme) setTheme(event.matches ? 'dark' : 'light');
  });
  function toggleDrawing() {
    var on = root.dataset.drawing !== 'true';
    root.dataset.drawing = String(on);
    drawingButton.setAttribute('aria-pressed', String(on));
    drawingButton.setAttribute('aria-label', on ? 'Hide drawing guides' : 'Show drawing guides');
  }
  drawingButton.addEventListener('click', toggleDrawing);
  document.addEventListener('keydown', function (event) {
    if (event.key.toLowerCase() === 'd' && !event.repeat && !event.ctrlKey && !event.metaKey && !event.altKey && !event.target.closest('input, textarea, select, [contenteditable]')) toggleDrawing();
  });
  var now = new Date();
  var date = document.getElementById('letterDate');
  date.textContent = new Intl.DateTimeFormat('en-GB', { day:'numeric', month:'long', year:'numeric', timeZone:'Asia/Kolkata' }).format(now);
  document.getElementById('localTime').textContent = new Intl.DateTimeFormat('en-GB', { hour:'2-digit', minute:'2-digit', timeZone:'Asia/Kolkata' }).format(now) + ' IST';
  date.dateTime = new Intl.DateTimeFormat('en-CA', { year:'numeric', month:'2-digit', day:'2-digit', timeZone:'Asia/Kolkata' }).format(now);
  document.getElementById('footerYear').textContent = now.getFullYear();
  function revealAnchor() {
    var target = document.getElementById(location.hash.slice(1));
    if (!target) return;
    for (var parent = target.parentElement; parent; parent = parent.parentElement) {
      if (parent.tagName === 'DETAILS') parent.open = true;
    }
    target.scrollIntoView();
  }
  window.addEventListener('hashchange', revealAnchor);
  if (location.hash) revealAnchor();
})();
