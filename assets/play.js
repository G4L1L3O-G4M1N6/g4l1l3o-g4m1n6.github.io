'use strict';
(() => {
  const games = JSON.parse(document.getElementById('demo-config').textContent);
  const player = document.getElementById('player');
  const placeholder = player.innerHTML;
  let lang = navigator.language.toLowerCase().startsWith('es') ? 'es' : 'en';
  let selected = 'corral';
  let feedback = '';
  const text = (en, es) => lang === 'es' ? es : en;
  function renderLanguage() {
    document.documentElement.lang = lang;
    document.querySelectorAll('[data-en][data-es]').forEach(el => { el.textContent = el.dataset[lang]; });
    const button = document.getElementById('language');
    button.textContent = lang === 'en' ? 'Español' : 'English';
    button.lang = lang === 'en' ? 'es' : 'en';
    const game = games[selected];
    document.getElementById('demo-description').textContent = game.text[lang === 'es' ? 3 : 2];
    const hook = document.getElementById('demo-hook');
    if (hook) hook.textContent = game.text[lang === 'es' ? 1 : 0];
  }
  function choose(slug) {
    if (!Object.hasOwn(games, slug)) slug = 'corral';
    selected = slug;
    player.innerHTML = placeholder;
    document.getElementById('demo-title').textContent = games[slug].name;
    document.getElementById('demo-icon').src = `/assets/games/${slug}/icon-160.webp`;
    document.querySelectorAll('[data-demo]').forEach(el => el.setAttribute('aria-pressed', String(el.dataset.demo === slug)));
    document.getElementById('restart').disabled = true;
    document.querySelector('#feedback [name=game]').value = slug;
    history.replaceState(null, '', `#demo=${slug}`);
    renderLanguage();
  }
  function start() {
    const frame = document.createElement('iframe');
    frame.title = `${games[selected].name} — browser demo`;
    frame.setAttribute('sandbox', 'allow-scripts');
    frame.referrerPolicy = 'no-referrer';
    frame.src = `/play/demos/${selected}.html`;
    player.replaceChildren(frame);
    document.getElementById('restart').disabled = false;
  }
  document.querySelectorAll('[data-demo]').forEach(el => el.addEventListener('click', () => choose(el.dataset.demo)));
  player.addEventListener('click', event => { if (event.target.closest('#start')) start(); });
  document.getElementById('restart').addEventListener('click', start);
  document.getElementById('language').addEventListener('click', () => { lang = lang === 'en' ? 'es' : 'en'; renderLanguage(); });
  document.getElementById('feedback').addEventListener('submit', event => {
    event.preventDefault();
    const answers = Object.fromEntries(new FormData(event.currentTarget));
    feedback = JSON.stringify({schema: 1, preview: 'galileo-2026-10-30', language: lang, ...answers}, null, 2);
    document.getElementById('feedback-text').value = feedback;
    document.getElementById('feedback-result').hidden = false;
    document.getElementById('feedback-status').textContent = text('Ready to copy or download. Nothing was sent.', 'Listo para copiar o descargar. No se envió nada.');
  });
  document.getElementById('copy-feedback').addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(feedback);
      document.getElementById('feedback-status').textContent = text('Copied. Share it with your inviter.', 'Copiado. Compártelo con quien te invitó.');
    } catch (_) {
      document.getElementById('feedback-text').select();
      document.getElementById('feedback-status').textContent = text('Select and copy the answers below.', 'Selecciona y copia las respuestas de abajo.');
    }
  });
  document.getElementById('download-feedback').addEventListener('click', () => {
    if (!feedback) return;
    const url = URL.createObjectURL(new Blob([feedback], {type: 'application/json'}));
    const link = document.createElement('a');
    link.href = url;
    link.download = 'galileo-feedback.json';
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  choose(new URLSearchParams(location.hash.slice(1)).get('demo') || 'corral');
})();
