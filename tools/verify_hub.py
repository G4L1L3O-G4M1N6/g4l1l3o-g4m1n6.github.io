"""Check the exact offline payloads and honest preview entry points."""
import hashlib
import json
from pathlib import Path
root = Path(__file__).resolve().parent.parent
manifest = json.loads((root / 'play/catalog.json').read_text())
assert set(manifest['demos']) == {'corral','eight-seconds','gold-shaft','tumbleweed','idle-rancher'}
for slug, info in manifest['demos'].items():
    data = (root / 'play/demos' / (slug + '.html')).read_bytes()
    assert len(data) == info['bytes'] <= 1048576
    assert hashlib.sha256(data).hexdigest() == info['sha256']
    assert b'"net":"preview"' in data
page = (root / 'play/index.html').read_text()
assert 'Install buttons are simulated' in page
assert "connect-src 'none'" in page
assert 'Nothing is sent automatically' in page
assert (root / 'CNAME').read_text().strip() == 'www.galileogamestudio.com'
print('Five exact preview payloads, browser-local feedback and stable domain verified')
