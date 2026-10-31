# Website validation hub — review draft

The studio home and five game pages now lead to `/play/`: one deliberately started/restartable demo at a time, English/Spanish hub text, honest accelerated-preview/English-gameplay disclosures, and a browser-local feedback export. Cattle Baron and Wildcatter remain concept pages without playable demos. The home removes the outdated hold instruction for Eight Seconds and an unsupported blanket claim about energy timers.

The five embedded HTML files are the exact current TestFlight review artifacts, checked against `play/catalog.json`. Frames permit scripts but do not share the parent origin. Feedback has no submission endpoint, email/name field, cookie, storage or analytics call. A tester explicitly copies/downloads their answers to share. Hosting still serves ordinary page/resource requests.

Existing feedback remains attributed to its original game when a visitor switches demos; editing answers invalidates any earlier prepared export.

Local and CI Chrome checks pass 24 cases across 360×800, 430×932, 768×1024 and 1280×900: each demo starts/restarts, only one iframe exists, language switches, feedback is generated locally, and the page has no horizontal overflow, external requests or script exceptions. [CI run 41150043282](https://github.com/G4L1L3O-G4M1N6/g4l1l3o-g4m1n6.github.io/actions/runs/41150043282) passes at cd74f55. Its 28 screenshots are retained; chooser, running Corral and feedback states were visually inspected at all four sizes. Screenshots are restricted to GitHub Actions. These checks do not establish physical Safari/audio/accessibility approval or measured product demand.

The two earlier CI runs passed their functional checks but failed while removing Chrome's temporary profile. Bounded filesystem retries fix that cleanup race; the successful run above includes it. No product assertion was removed.

This branch is a review draft. Martin's revised creative approval is still pending; no ad spend is active. Existing game policy body text is unchanged in this branch (only shared navigation gains the demo link). The separately prepared age-aware policy drafts remain in `g4l1l3o-site-audience` and require matching audience/store/vendor review. This branch does not publish them or establish legal clearance.

Local preview: `python3 -m http.server 8765 --bind 127.0.0.1` from this checkout, then open `http://127.0.0.1:8765/play/`. Regenerate with `python3 build.py` using Pillow. Browser checks: `node tools/review.mjs`; catalog check: `python3 tools/verify_hub.py`.
