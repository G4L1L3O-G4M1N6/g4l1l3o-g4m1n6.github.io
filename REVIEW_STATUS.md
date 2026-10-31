# Website validation hub — review draft

The studio home and five game pages now lead to `/play/`: one deliberately started/restartable demo at a time, English/Spanish hub text, honest accelerated-preview/English-gameplay disclosures, and a browser-local feedback export. Cattle Baron and Wildcatter remain concept pages without playable demos. The home removes the outdated hold instruction for Eight Seconds and an unsupported blanket claim about energy timers.

The five embedded HTML files are the exact current TestFlight review artifacts, checked against `play/catalog.json`. Frames permit scripts but do not share the parent origin. Feedback has no submission endpoint, email/name field, cookie, storage or analytics call. A tester explicitly copies/downloads their answers to share. Hosting still serves ordinary page/resource requests.

Existing feedback remains attributed to its original game when a visitor switches demos; editing answers invalidates any earlier prepared export.

Local Chrome checks pass24 cases across360x800,430x932,768x1024 and1280x900: each demo starts/restarts, only one iframe exists, language switches, feedback is generated locally, and the page has no horizontal overflow, external requests or script exceptions. Screenshots are restricted to GitHub Actions; current branch CI will retain four-size captures and logs. These checks do not establish physical Safari/audio/accessibility approval or measured product demand.

This branch is a review draft. Martin's revised creative approval is still pending; no ad spend is active. Existing game policy body text is unchanged in this branch (only shared navigation gains the demo link). The separately prepared age-aware policy drafts remain in `g4l1l3o-site-audience` and require matching audience/store/vendor review. This branch does not publish them or establish legal clearance.

Local preview: `python3 -m http.server 8765 --bind 127.0.0.1` from this checkout, then open `http://127.0.0.1:8765/play/`. Regenerate with `python3 build.py` using Pillow. Browser checks: `node tools/review.mjs`; catalog check: `python3 tools/verify_hub.py`.
