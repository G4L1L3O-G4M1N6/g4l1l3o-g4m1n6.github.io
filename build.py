#!/usr/bin/env python3
"""Generates the G4L1L3O G4M1N6 policy site (GitHub Pages, org site).

One privacy policy and one terms page per game, from the same template,
so every app's store listing has a stable URL:
  https://g4l1l3o-g4m1n6.github.io/<slug>/privacy
  https://g4l1l3o-g4m1n6.github.io/<slug>/terms
Run: python3 build.py  (writes the HTML next to this file)
"""
import html, pathlib

ROOT = pathlib.Path(__file__).parent
CONTACT = "bkimartinsuarez@gmail.com"
EFFECTIVE = "October 28, 2026"

GAMES = [
    {"slug": "texas-rodeo", "name": "Texas Rodeo", "iap": "optional in-app purchases including virtual currency (Belt Buckles), cosmetic items, boosts, and ad removal"},
    {"slug": "eight-seconds", "name": "Eight Seconds: Bull Ride", "iap": "an optional \"Remove Ads\" purchase"},
    {"slug": "corral", "name": "Corral: Fence Puzzle", "iap": "an optional \"Remove Ads\" purchase"},
    {"slug": "tumbleweed", "name": "Tumbleweed Golf", "iap": "an optional \"Remove Ads\" purchase"},
    {"slug": "gold-shaft", "name": "Gold Shaft: Idle Miner", "iap": "an optional \"Remove Ads\" purchase and an optional \"Permanent x2 Income\" purchase"},
    {"slug": "idle-rancher", "name": "Idle Rancher: Cozy Ranch", "iap": "an optional \"Remove Ads\" purchase and an optional \"Permanent x2 Income\" purchase"},
    {"slug": "cattle-baron", "name": "Cattle Baron: Ranch Tycoon", "iap": "an optional \"Remove Ads\" purchase and an optional \"Permanent x2 Income\" purchase"},
    {"slug": "wildcatter", "name": "Wildcatter: Oil Tycoon", "iap": "an optional \"Remove Ads\" purchase and an optional \"Permanent x2 Income\" purchase"},
]

STYLE = """
body { font-family: Georgia, serif; max-width: 640px; margin: 2rem auto; padding: 0 1rem; color: #2c1e0e; line-height: 1.6; background: #fdf8ef; }
h1 { color: #7a4a12; font-size: 1.5rem; } h2 { color: #7a4a12; font-size: 1.1rem; margin-top: 1.5rem; }
.date { color: #888; font-size: 0.9rem; } ul { padding-left: 1.5rem; } a { color: #9a5a14; }
"""


def page(title, body):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title><style>{STYLE}</style></head>
<body>
{body}
<p><a href="/">G4L1L3O G4M1N6 games</a></p>
</body></html>
"""


def privacy(g):
    n = html.escape(g["name"])
    return page(f"{g['name']} — Privacy Policy", f"""
<h1>{n} — Privacy Policy</h1>
<p class="date">Effective date: {EFFECTIVE}</p>
<h2>1. Overview</h2>
<p>{n} ("the Game") is developed by Martin Suarez (G4L1L3O G4M1N6). This policy explains what data the Game handles, how it is used, and your choices.</p>
<h2>2. Data stored on your device</h2>
<ul><li><b>Save data:</b> game progress and settings, stored in a local file on your device. It is never sent to us.</li></ul>
<h2>3. Data collected by third-party services</h2>
<ul>
<li><b>Google AdMob</b> (ads): may collect device identifiers, IP address, and ad interaction data to serve and measure ads. See <a href="https://policies.google.com/privacy">Google's Privacy Policy</a>.</li>
<li><b>Apple App Store / StoreKit</b> and <b>Google Play Billing</b> (purchases): purchases are processed by Apple or Google. See <a href="https://www.apple.com/legal/privacy/">Apple's Privacy Policy</a> and <a href="https://policies.google.com/privacy">Google's Privacy Policy</a>.</li>
</ul>
<h2>4. Data we do not collect</h2>
<ul><li>No name, email, phone number, precise location, contacts, or account.</li><li>We run no servers that receive your data, and we do not sell your personal data. Data is shared with Google AdMob only as described in section 5.</li></ul>
<h2>5. Advertising, tracking and your choices</h2>
<p>The Game shows ads from Google AdMob, including optional ads you choose to watch for in-game rewards. If you allow it, ads may be personalized using your device's advertising identifier and ad interaction data; this may be considered "sharing" for cross-context behavioral advertising under some US state laws.</p>
<ul>
<li><b>iOS:</b> the Game asks for your permission (App Tracking Transparency) before any cross-app tracking. If you decline, you still get the full game with non-personalized ads. You can change this at any time in Settings → Privacy &amp; Security → Tracking.</li>
<li><b>EU, UK and certain US states:</b> the Game shows a consent / privacy-choices form provided by Google before personalized ads are used. You can review or change your choices at any time from the Game's Settings → Privacy choices.</li>
<li><b>Android:</b> you can reset or delete your advertising ID and limit personalized ads in your device's Google settings.</li>
</ul>
<p>The optional "Remove Ads" purchase removes non-optional ads.</p>
<h2>6. Children</h2>
<p>The Game is not directed at children under 13, and we do not knowingly collect personal information from children. If you believe a child has provided personal data, contact us and we will help remove it.</p>
<h2>7. Data retention and your rights</h2>
<p>Game data stays on your device until you delete the Game or its data. We hold no server-side data about you to access, correct, or delete. For data handled by Google or Apple, use their privacy tools.</p>
<h2>8. Changes</h2>
<p>We may update this policy; the effective date above shows the latest revision.</p>
<h2>9. Contact</h2>
<p>Questions? Email <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>
""")


def terms(g):
    n = html.escape(g["name"])
    return page(f"{g['name']} — Terms of Service", f"""
<h1>{n} — Terms of Service</h1>
<p class="date">Effective date: {EFFECTIVE}</p>
<h2>1. Acceptance</h2><p>By downloading, installing, or playing {n} ("the Game"), you agree to these Terms. If you do not agree, do not use the Game.</p>
<h2>2. License</h2><p>We grant you a limited, non-exclusive, non-transferable, revocable license to use the Game for personal, non-commercial entertainment on devices you own.</p>
<h2>3. In-app purchases</h2><p>The Game offers {html.escape(g["iap"])}. Purchases are final except where required by law or by the policies of the Apple App Store or Google Play. Virtual items have no real-world value.</p>
<h2>4. Conduct</h2><p>Do not modify, reverse-engineer, or decompile the Game, or tamper with save data or purchase verification.</p>
<h2>5. Save data</h2><p>Progress is stored on your device. We are not responsible for progress lost through device failure, uninstalling, or data corruption.</p>
<h2>6. Intellectual property</h2><p>The Game's content is owned by Martin Suarez or licensed from third-party creators (see the in-game Credits and Open-source licences screens).</p>
<h2>7. Disclaimer</h2><p>The Game is provided "as is", without warranties of any kind.</p>
<h2>8. Limitation of liability</h2><p>To the maximum extent permitted by law, we are not liable for indirect, incidental, special, consequential, or punitive damages arising from your use of the Game.</p>
<h2>9. Changes</h2><p>We may update these Terms; the effective date above shows the latest revision.</p>
<h2>10. Contact</h2><p>Questions? Email <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>
""")


def main():
    items = []
    for g in GAMES:
        d = ROOT / g["slug"]
        d.mkdir(exist_ok=True)
        (d / "privacy.html").write_text(privacy(g))
        (d / "terms.html").write_text(terms(g))
        items.append(f'<li>{html.escape(g["name"])} — <a href="/{g["slug"]}/privacy">Privacy Policy</a> · <a href="/{g["slug"]}/terms">Terms</a></li>')
    (ROOT / "index.html").write_text(page("G4L1L3O G4M1N6", "<h1>G4L1L3O G4M1N6</h1><p>Small games by Martin Suarez.</p><ul>" + "".join(items) + "</ul>"))
    (ROOT / ".nojekyll").write_text("")


if __name__ == "__main__":
    main()
