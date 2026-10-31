"""Build a static, tracker-free demo and feedback hub from verified offline previews."""
import hashlib
import json
import shutil
from pathlib import Path

SLUGS = ['corral', 'eight-seconds', 'gold-shaft', 'tumbleweed', 'idle-rancher']
TEXT = {
    'corral': ('Fence the herd', 'Encierra al rebaño', 'Three puzzles. Limited pieces. A wolf to outsmart.', 'Tres retos, cercas limitadas y un lobo que anticipar.'),
    'eight-seconds': ('Ride the next bull', 'Domina al siguiente toro', 'Flick with each buck through three eight-second rides.', 'Desliza con cada salto en tres montas de ocho segundos.'),
    'gold-shaft': ('Build a better mine', 'Haz crecer tu mina', 'Hold to dig, hire a crew and clear the hauling bottleneck.', 'Mantén pulsado para excavar, contrata mineros y mejora el transporte.'),
    'tumbleweed': ('Find your line', 'Encuentra tu trayectoria', 'Four desert holes, three lives and a perk that changes your run.', 'Cuatro hoyos, tres vidas y una mejora que cambia tu partida.'),
    'idle-rancher': ('Put your ranch to work', 'Pon a trabajar tu rancho', 'Collect, automate and choose how to grow across three market trips.', 'Recolecta, automatiza y decide cómo crecer en tres viajes al mercado.'),
}


def build(root, games):
    root = Path(root)
    source = root.parent / 'playables-testflight' / 'dist'
    folder = root / 'play'
    demos = folder / 'demos'
    demos.mkdir(parents=True, exist_ok=True)
    manifest = {'schema': 1, 'kind': 'accelerated-browser-previews', 'demos': {}}
    by_slug = {g['slug']: g for g in games}
    for slug in SLUGS:
        origin = source / slug / 'preview.html'
        target = demos / (slug + '.html')
        if origin.exists():
            shutil.copyfile(origin, target)
        data = target.read_bytes()
        if b'"net":"preview"' not in data or len(data) > 1048576:
            raise ValueError('Expected verified offline preview: ' + slug)
        manifest['demos'][slug] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    (folder / 'catalog.json').write_text(json.dumps(manifest, indent=2) + '\n')
    cards = []
    for slug in SLUGS:
        g = by_slug[slug]
        en, es, description_en, description_es = TEXT[slug]
        cards.append(f'''<button class="demo-choice" type="button" data-demo="{slug}" aria-pressed="false">
          <img src="/assets/games/{slug}/icon-160.webp" width="52" height="52" alt="">
          <span><strong>{g['short']}</strong><small data-en="{en}" data-es="{es}">{en}</small></span><span aria-hidden="true">→</span>
        </button>''')
    options = lambda items: ''.join(f'<option value="{value}" data-en="{en}" data-es="{es}">{en}</option>' for value, en, es in items)
    yes_no = options([('', 'Choose an answer', 'Elige una respuesta'), ('yes', 'Yes', 'Sí'), ('partly', 'Partly', 'Más o menos'), ('no', 'No', 'No')])
    again = options([('', 'Choose an answer', 'Elige una respuesta'), ('yes', 'Yes', 'Sí'), ('maybe', 'Maybe', 'Tal vez'), ('no', 'No', 'No')])
    body = '''<link rel="stylesheet" href="/assets/play.css">
<section class="try-hero wrap">
  <div class="try-heading"><p class="eyebrow" data-en="THE GALILEO PLAYGROUND" data-es="PRUEBA GALILEO">THE GALILEO PLAYGROUND</p>
  <button id="language" class="language" type="button" lang="es">Español</button></div>
  <h1 data-en="A small game. A good minute." data-es="Un pequeño juego. Un gran momento.">A small game. A good minute.</h1>
  <p class="try-lede" data-en="Pick a game, try its first challenge and tell us what you think. No download or account needed." data-es="Elige un juego, prueba su primer reto y cuéntanos qué te parece. Sin descargas ni cuentas.">Pick a game, try its first challenge and tell us what you think. No download or account needed.</p>
  <p class="demo-disclosure" data-en="These are short, accelerated browser previews. No real ads or purchases. Install buttons are simulated; the full iPhone games are still in testing. The demos currently use English." data-es="Son demos cortas y aceleradas para el navegador. No hay anuncios ni compras reales. Los botones de instalación son simulados; los juegos completos para iPhone siguen en pruebas. Las demos están en inglés.">These are short, accelerated browser previews. No real ads or purchases. Install buttons are simulated; the full iPhone games are still in testing. The demos currently use English.</p>
</section>
<section class="wrap playground" aria-label="Game demos">
  <div class="demo-sidebar"><h2 data-en="Choose your next minute" data-es="Elige tu próximo reto">Choose your next minute</h2>
    <div class="demo-choices">''' + ''.join(cards) + '''</div>
    <p class="coming-demos" data-en="Cattle Baron and Wildcatter are also in development. Their browser demos are coming later." data-es="Cattle Baron y Wildcatter también están en desarrollo. Sus demos para navegador llegarán después.">Cattle Baron and Wildcatter are also in development. Their browser demos are coming later.</p>
  </div>
  <div class="demo-stage"><div class="demo-stage-heading"><div><h2 id="demo-title">Corral</h2><p id="demo-description"></p></div>
    <button id="restart" class="language" type="button" disabled data-en="Restart" data-es="Reiniciar">Restart</button></div>
    <div class="phone-preview" id="player"><div class="demo-placeholder"><img id="demo-icon" src="/assets/games/corral/icon-160.webp" width="90" height="90" alt="">
      <p id="demo-hook">Fence the herd</p><button id="start" class="button" type="button" data-en="Play the demo" data-es="Jugar la demo">Play the demo</button>
      <small data-en="Use touch or a mouse. Sound starts with your tap." data-es="Usa la pantalla táctil o el ratón. El sonido inicia al tocar.">Use touch or a mouse. Sound starts with your tap.</small></div></div>
    <p class="demo-footnote" data-en="Try one game first. Use Choose your next minute to switch games." data-es="Empieza con un juego. Usa Elige tu próximo reto para cambiar de demo.">Try one game first. Use Choose your next minute to switch games.</p>
  </div>
</section>
<section class="wrap feedback-section" aria-labelledby="feedback-heading"><div>
  <p class="eyebrow" data-en="HELP SHAPE THE NEXT VERSION" data-es="AYUDA A MEJORAR LA SIGUIENTE VERSIÓN">HELP SHAPE THE NEXT VERSION</p>
  <h2 id="feedback-heading" data-en="Worth another round?" data-es="¿Una partida más?">Worth another round?</h2>
  <p data-en="Your honest reaction matters more than a perfect score. No names, email addresses or other personal information, please." data-es="Tu opinión honesta vale más que una puntuación perfecta. No incluyas nombres, correos ni otros datos personales.">Your honest reaction matters more than a perfect score. No names, email addresses or other personal information, please.</p>
  <p class="feedback-local" data-en="This form stays in your browser. Copy or download your answers and share them with the person who invited you. Nothing is sent automatically or saved by this site." data-es="El formulario permanece en tu navegador. Copia o descarga tus respuestas y compártelas con quien te invitó. El sitio no envía ni guarda tus respuestas automáticamente.">This form stays in your browser. Copy or download your answers and share them with the person who invited you. Nothing is sent automatically or saved by this site.</p>
</div><form id="feedback"><label><span data-en="Which game did you try?" data-es="¿Qué juego probaste?">Which game did you try?</span><select name="game" required>''' + ''.join(f'<option value="{s}">{by_slug[s]["short"]}</option>' for s in SLUGS) + '''</select></label>
  <label><span data-en="Was the first action clear?" data-es="¿Quedó clara la primera acción?">Was the first action clear?</span><select name="clear" required>''' + yes_no + '''</select></label>
  <label><span data-en="Would you play another round?" data-es="¿Jugarías otra partida?">Would you play another round?</span><select name="again" required>''' + again + '''</select></label>
  <label><span data-en="Did anything break?" data-es="¿Algo falló?">Did anything break?</span><select name="bug" required>''' + options([('', 'Choose an answer', 'Elige una respuesta'), ('no', 'No', 'No'), ('controls', 'Controls', 'Controles'), ('layout', 'Layout or text', 'Diseño o texto'), ('loading', 'Loading or sound', 'Carga o sonido'), ('other', 'Something else', 'Otra cosa')]) + '''</select></label>
  <label class="full"><span data-en="What would make it better? (optional)" data-es="¿Qué lo haría mejor? (opcional)">What would make it better? (optional)</span><textarea name="note" maxlength="800" rows="3"></textarea></label>
  <div class="full feedback-actions"><button class="button" type="submit" data-en="Prepare my feedback" data-es="Preparar mis respuestas">Prepare my feedback</button><button class="language" type="reset" data-en="New response" data-es="Nueva respuesta">New response</button><span id="feedback-status" role="status" aria-live="polite"></span></div>
  <div class="full" id="feedback-result" hidden><label for="feedback-text" data-en="Your feedback to share" data-es="Tus respuestas para compartir">Your feedback to share</label><textarea id="feedback-text" readonly rows="8"></textarea><div class="feedback-actions"><button id="copy-feedback" type="button" class="language" data-en="Copy answers" data-es="Copiar respuestas">Copy answers</button><button id="download-feedback" type="button" class="language" data-en="Download answers" data-es="Descargar respuestas">Download answers</button></div></div>
</form></section><script src="/assets/play.js" defer></script>'''
    config = {s: {'name': by_slug[s]['short'], 'text': list(TEXT[s])} for s in SLUGS}
    body += '<script id="demo-config" type="application/json">' + json.dumps(config).replace('<', '\\u003c') + '</script>'
    return body
