#!/usr/bin/env python3
"""Generates galileogamestudio.com (GitHub Pages, org site, custom domain via CNAME).

Pages:
  /                       studio home: hero, game lineup, about, contact
  /<slug>/                one page per listed game (screenshots, features, help links)
  /<slug>/privacy|terms|support   policy pages (stable URLs used by the apps,
                          AdMob and App Store Connect: never rename them)
  /support/               every game's support and policy links
  /404.html, /sitemap.xml, /robots.txt, social preview images

Adding a game = one entry in GAMES (see SOP_NEW_GAME.md section 5.5), then
  python3 build.py
Images (icons, screenshots, social previews) are made from the game folders next to
this repo (../<game>/icon.png, ../ci_shots/<game>/430x932/...). If a source is missing
the existing file under assets/ is kept, so the build also works on a fresh clone.
Needs Pillow (pip install pillow).
"""
import html, pathlib, random, datetime

ROOT = pathlib.Path(__file__).parent
WORKSPACE = ROOT.parent  # ~/Code/G4L1L3O-G4M1N6
SITE = "https://www.galileogamestudio.com"
STUDIO = "Galileo Gaming"
LEGAL_NAME = "Galileo Gaming Studio by Martin Suarez"
CONTACT = "support@galileogamestudio.com"
EFFECTIVE = "October 28, 2026"
YEAR = 2026

# One entry per game. Fields:
#   slug         URL folder, never change once live (policy URLs are in the app and stores)
#   name         exact App Store name (used on the policy pages)
#   short        display name on the site
#   listed       False = policy pages only, not shown in the lineup (default True)
#   subtitle     App Store subtitle (30 characters max)
#   pitch        2-3 sentences, from store/listing.md
#   features     3-4 short lines, from the listing description
#   tags         genre tags
#   accent       the game's own color (hex), used for its band and page header
#   icon         path of the icon, relative to the workspace
#   shots        [(path relative to ci_shots/<slug>/430x932/, alt text)], 3-5 gameplay frames;
#                the first 3 show on the home page
#   app_store    App Store URL; "" shows "Coming soon to the App Store", a URL shows
#                Apple's official badge
#   cloud        False = progress is not synced (support page wording); default True
#   iap          every in-app purchase, as listed in the Terms
GAMES = [
    {
        "slug": "eight-seconds", "name": "Eight Seconds: Bull Ride", "short": "Eight Seconds",
        "subtitle": "One-thumb rodeo. Hold on.",
        "pitch": "Hold your thumb down, swipe with every buck, and try to last eight seconds on the bull. "
                 "Perfect swipes build a streak and get the crowd roaring, and every eight seconds the bull gets meaner.",
        "features": ["One thumb and a few seconds a ride", "The Daily Bull: everyone rides the same bull today",
                     "Collect bulls and riders, and upgrade your gear from ranch plain to legendary gold",
                     "Plays offline"],
        "tags": ["Arcade", "Rodeo", "One thumb"], "accent": "#D9732F",
        "icon": "eight-seconds/icon.png",
        "shots": [("daily/07_autoride_9.png", "A rider holding on to a bucking bull at 9.13 seconds, with a GREAT x4 streak pop"),
                  ("collection_settings/01_boot.png", "The home screen: a rider on a bull in front of a desert sunset arena"),
                  ("collection_settings/02_tapnode_Tab_bulls.png", "The bulls collection, with coats and bull stock to unlock"),
                  ("daily/19_tap_DAILY BULL.png", "The Daily Bull screen with the day streak and today's ride"),
                  ("first_launch/19_wait_0.3.png", "A New Best result card: 26.86 seconds and a Ride Again button")],
        "app_store": "", "iap": "an optional \"Remove Ads\" purchase",
    },
    {
        "slug": "corral", "name": "Corral: Fence Puzzle", "short": "Corral",
        "subtitle": "Fence-building block puzzle",
        "pitch": "Drag fence pieces onto the pasture and close pens around the animals. "
                 "The bigger the herd you round up at once, the bigger the score. No timer, no rush, just one more move.",
        "features": ["A new daily board, the same for everyone", "Fill your barn with every animal you pen",
                     "Earn painted, stone and iron fences, and autumn and snowy pastures", "No timer and no Wi-Fi needed"],
        "tags": ["Puzzle", "Block puzzle", "Relaxing"], "accent": "#4E8A3A",
        "icon": "corral/icon.png",
        "shots": [("first_launch/43_autoplay_2.png", "A pasture board with wooden fence pens around cows and sheep, score 360"),
                  ("first_launch/13_autoplay_4.png", "Two closed pens on the board and a x1.5 streak"),
                  ("navigation/22_autoplay_3.png", "Today's Roundup: pen 7 animals in 33 pieces"),
                  ("collection/05_tap_OPEN THE BARN.png", "The barn: fences, pastures and herd accessories to unlock"),
                  ("navigation/15_tapnode_DailyTab.png", "The Daily Roundup calendar with the day streak")],
        "app_store": "", "iap": "an optional \"Remove Ads\" purchase",
    },
    {
        "slug": "tumbleweed", "name": "Tumbleweed: Desert Golf", "short": "Tumbleweed",
        "subtitle": "Endless, quiet desert golf",
        "pitch": "Drag back, let go, and watch the tumbleweed roll across the desert toward the flag. "
                 "Every hole flows straight into the next, with no menus, just the sun going down over an endless course.",
        "features": ["One finger: drag back to aim, let go to throw", "Today's 9: nine new holes each day, one par for everyone",
                     "A scorecard every 18 holes, and your best 18 to beat", "Earn tumbleweeds, trails, flags and skies by playing"],
        "tags": ["Golf", "Casual", "Relaxing"], "accent": "#8A4F7D",
        "icon": "tumbleweed/icon.png",
        "shots": [("first_launch/01_boot.png", "The Tumbleweed title over a desert sunset: a quiet game of desert golf"),
                  ("first_launch/10_solvehole.png", "Hole 1 in one stroke, and a new Golden tumbleweed unlocked"),
                  ("reset/01_boot.png", "A flag on a desert ridge at hole 9, with Today's 9 below"),
                  ("visual/23_wait_0.6.png", "Hole 24 at dusk, the sun sitting behind the mesas")],
        "app_store": "", "iap": "an optional \"Remove Ads\" purchase",
    },
    {
        "slug": "gold-shaft", "name": "Gold Shaft: Idle Miner", "short": "Gold Shaft",
        "subtitle": "Tap, dig and strike it rich",
        "pitch": "Tap the rock and start digging. Hire miners, lay track for the carts and send the elevator deeper, "
                 "from dirt to clay to magma. When the shaft runs dry, strike the Mother Lode and start again richer.",
        "features": ["One-thumb tap-to-dig with crits and boulder bonuses",
                     "Miners, carts, lanterns and an elevator through eight layers of rock",
                     "Rare gems hidden in glinting nuggets", "Your mine keeps digging while you're away"],
        "tags": ["Idle", "Clicker", "Mining"], "accent": "#B07A1E",
        "icon": "gold-shaft/icon.png",
        "shots": [("deep/27_tapmany_MineView,20.png", "Deep in the magma layer: a critical hit for 250K gold and a golden tower"),
                  ("deep/20_tapnode_Buy_elevator.png", "The shaft at the gem caves with the upgrades list for pickaxe, miners and carts"),
                  ("features/33_tapnode_GlintNugget.png", "A glinting nugget found: +1.80K and a quartz for the collection"),
                  ("prestige/18_tapnode_Tab_prestige.png", "The Mother Lode screen: 20 nuggets, +200% income"),
                  ("first_launch/28_notify_resumed.png", "While you were gone: +3.60K gold, with a Collect x2 button")],
        "app_store": "", "iap": "an optional \"Remove Ads\" purchase and an optional \"Permanent x2 Income\" purchase",
    },
    {
        "slug": "idle-rancher", "name": "Idle Rancher: Cozy Ranch", "short": "Idle Rancher",
        "subtitle": "Cozy idle farm & ranch",
        "pitch": "Start with a few hens and a corn row, and grow a ranch that runs itself. "
                 "Unlock cows, sheep, pigs, goats and horses, fill your neighbours' orders, and take your best herds to the County Fair.",
        "features": ["Hire ranch hands and send the market truck to town", "Earn flower beds, beehives and a windmill",
                     "Your ranch keeps earning while you're away", "Gentle music, no energy, no timers to babysit"],
        "tags": ["Idle", "Farming", "Cozy"], "accent": "#3F8FC4",
        "icon": "idle-rancher/icon.png",
        "shots": [("showcase/68_expect_ranch.png", "A full ranch: horses, pumpkins, pigs, cows, sheep and corn around the red barn"),
                  ("showcase/34_scrollto_Buy_horse.png", "The animals list: hens, corn, cows, sheep, pumpkins, pigs, goats and horses"),
                  ("first_launch/19_tapnode_OrdersButton.png", "Neighbours' orders for eggs, with coin rewards"),
                  ("returning/35_tap_WIN MY RIBBONS.png", "Blue ribbon at the County Fair: the judges loved your ranch"),
                  ("returning/01_boot.png", "Welcome back: your ranch earned 3.60K while you were away")],
        "app_store": "", "iap": "an optional \"Remove Ads\" purchase and an optional \"Permanent x2 Income\" purchase",
    },
    {
        "slug": "cattle-baron", "name": "Cattle Baron: Ranch Tycoon", "short": "Cattle Baron",
        "subtitle": "Idle ranch business tycoon",
        "pitch": "Sell your first eggs from a roadside stand, then buy the cornfield, the dairy barn, the stables and the rail depot. "
                 "Hire foremen to run each business, ride out the seasons, and pass down the Family Brand.",
        "features": ["10 ranch enterprises, each growing through three stages", "10 foremen to hire and 25 ranch upgrades",
                     "Four seasons, and market telegrams with choices to make", "Your foremen keep working while you're away"],
        "tags": ["Idle", "Tycoon", "Ranch"], "accent": "#B8332A",
        "icon": "cattle-baron/icon.png",
        "shots": [("offline_prestige/05_wait_1.8.png", "A ranch empire worth $1.71B: poultry barn, dairy farm, horse ranch and feed store"),
                  ("first_launch/11_tapnode_Hire0.png", "The foremen: Hattie is hired to run the egg stand"),
                  ("first_launch/24_tapnode_Upgrade_irrigation.png", "A County Fair telegram: sell now or wait for a better price"),
                  ("first_launch/35_tapnode_SeasonChip.png", "The ranch year: calving season, summer dry spell, fall auction and winter feed"),
                  ("offline_prestige/09_tapnode_PassDownButton.png", "Pass down the brand: your heirs start over with 12 brand points")],
        "app_store": "", "iap": "an optional \"Remove Ads\" purchase and an optional \"Permanent x2 Income\" purchase",
    },
    {
        "slug": "wildcatter", "name": "Wildcatter: Oil Tycoon", "short": "Wildcatter",
        "subtitle": "Idle Texas oil tycoon",
        "pitch": "Survey the lease, drill your first well, and pipe the crude to your tanks. "
                 "Then watch the price: booms, busts and Gulf hurricanes move the market, and you decide when to hold and when to sell.",
        "features": ["Seismic surveys show dry, fair, rich or gusher-prone ground", "Pumpjacks, pipelines and tanks you can see working",
                     "Tap gushers fast for a pile of cash", "Sell the lease and wildcat a richer basin, from the Permian to offshore"],
        "tags": ["Idle", "Tycoon", "Oil"], "accent": "#C9A000",
        "icon": "wildcatter/icon.png",
        "shots": [("oilfield/47_wait_6.5.png", "Gusher! You capped it and sold the spill for $1.77K"),
                  ("oilfield/21_tapfield_well.png", "The oil field with a pumpjack, a refinery and the live oil price"),
                  ("oilfield/56_expect_text_HOLDING.png", "The market: oil at $45.58, holding the barrels until the price is right"),
                  ("prestige/03_tapnode_SaleButton.png", "Sell the field: the next lease is on the Gulf Coast, +20 royalties"),
                  ("prestige/15_tapnode_CollectionButton.png", "The collection: field themes, company paint and logos")],
        "app_store": "", "iap": "an optional \"Remove Ads\" purchase and an optional \"Permanent x2 Income\" purchase",
    },
    # Older title, being rewritten: policy pages only until the new version ships.
    {"slug": "texas-rodeo", "name": "Texas Rodeo", "short": "Texas Rodeo", "listed": False, "icon": "texas-rodeo/icon.png", "cloud": False,
     "iap": "optional in-app purchases including virtual currency (Belt Buckles), cosmetic items, boosts, and ad removal"},
]

LISTED = [g for g in GAMES if g.get("listed", True)]
e = html.escape


# ---------------------------------------------------------------- images

def build_images():
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Pillow not installed: keeping existing images")
        return
    A = ROOT / "assets"
    (A / "games").mkdir(parents=True, exist_ok=True)
    fonts = {"lilita": WORKSPACE / "cattle-baron/assets/fonts/lilita_one/LilitaOne-Regular.ttf",
             "nunito": WORKSPACE / "idle-rancher/assets/fonts/nunito/Nunito-Variable.ttf"}

    def font(kind, size, weight=None):
        f = ImageFont.truetype(str(fonts[kind]), size)
        if weight:
            f.set_variation_by_axes([weight])
        return f

    def fit(text, kind, size, maxw, weight=None):
        while size > 12:
            f = font(kind, size, weight)
            if f.getlength(text) <= maxw:
                return f
            size -= 2
        return f

    def rounded(im, size, r=0.225):
        im = im.convert("RGBA").resize((size, size), Image.LANCZOS)
        mask = Image.new("L", (size * 4, size * 4), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, size * 4 - 1, size * 4 - 1), int(size * 4 * r), fill=255)
        im.putalpha(mask.resize((size, size), Image.LANCZOS))
        return im

    def night(w, h, seed=3):
        bg = Image.new("RGB", (w, h), "#0F1229")
        d = ImageDraw.Draw(bg)
        rnd = random.Random(seed)
        for _ in range(int(w * h / 4000)):
            x, y, r = rnd.randrange(w), rnd.randrange(h), rnd.choice([1, 1, 1, 2])
            d.ellipse((x, y, x + r, y + r), fill=rnd.choice(["#3C4270", "#5A6096", "#8C92C2"]))
        return bg

    # Site icons from the logo: the telescope and star, without the wordmark.
    logo_path = WORKSPACE / "brand/galileo_logo.png"
    if logo_path.exists():
        logo = Image.open(logo_path).convert("RGB")
        mark = logo.crop((280, 190, 750, 660))
        for size, name in [(32, "favicon-32.png"), (180, "apple-touch-icon.png"), (192, "icon-192.png"), (512, "icon-512.png")]:
            mark.resize((size, size), Image.LANCZOS).save(A / name, optimize=True)
        mark.resize((96, 96), Image.LANCZOS).save(A / "mark-96.webp", quality=90)
        logo.resize((320, 320), Image.LANCZOS).save(A / "logo-320.webp", quality=88)

    have_fonts = all(p.exists() for p in fonts.values())
    for g in GAMES:
        if "icon" not in g:
            continue
        d = A / "games" / g["slug"]
        d.mkdir(parents=True, exist_ok=True)
        icon_src = WORKSPACE / g["icon"]
        if icon_src.exists():
            ic = Image.open(icon_src).convert("RGB")
            for size in (160, 320):
                ic.resize((size, size), Image.LANCZOS).save(d / f"icon-{size}.webp", quality=88)
        if not g.get("listed", True):
            continue
        shots_dir = WORKSPACE / "ci_shots" / g["slug"] / "430x932"
        for i, (src, _alt) in enumerate(g["shots"], 1):
            p = shots_dir / src
            if p.exists():
                out = d / f"shot-{i}.webp"
                q = 82
                while True:
                    Image.open(p).convert("RGB").save(out, quality=q, method=6)
                    if out.stat().st_size <= 150_000 or q <= 50:
                        break
                    q -= 8
        # Social preview, 1200x630.
        if icon_src.exists() and have_fonts:
            og = night(1200, 630, seed=len(g["slug"]))
            dr = ImageDraw.Draw(og)
            dr.rectangle((0, 610, 1200, 630), fill=g["accent"])
            og.paste(rounded(Image.open(icon_src), 300), (90, 150), rounded(Image.open(icon_src), 300))
            shot1 = shots_dir / g["shots"][0][0]
            x = 450
            if shot1.exists():
                ph = Image.open(shot1).convert("RGB").resize((236, 512), Image.LANCZOS)
                frame = Image.new("RGB", (252, 528), "#000000")
                frame.paste(ph, (8, 8))
                m = Image.new("L", (252, 528), 0)
                ImageDraw.Draw(m).rounded_rectangle((0, 0, 251, 527), 34, fill=255)
                og.paste(frame, (890, 70), m)
            dr.text((x, 190), g["short"], font=fit(g["short"], "lilita", 84, 410), fill="#FFF3C4")
            dr.text((x, 298), g["subtitle"], font=fit(g["subtitle"], "nunito", 38, 410, 700), fill="#C9CDE6")
            dr.text((x, 380), "Coming soon to the App Store" if not g["app_store"] else "On the App Store",
                    font=fit("Coming soon to the App Store", "nunito", 30, 410, 800), fill="#FACC4C")
            dr.text((x, 520), STUDIO, font=font("lilita", 34), fill="#8C92C2")
            og.save(d / "og.jpg", quality=86, optimize=True)

    if have_fonts:
        og = night(1200, 630, seed=11)
        dr = ImageDraw.Draw(og)
        if logo_path.exists():
            m = Image.open(logo_path).convert("RGB").crop((250, 130, 790, 670)).resize((150, 150), Image.LANCZOS)
            og.paste(m, (80, 60))
        dr.text((250, 95), STUDIO, font=font("lilita", 64), fill="#FACC4C")
        dr.text((84, 240), "Small games with a western heart.", font=font("lilita", 66), fill="#FFF3C4")
        n = len(LISTED)
        size = min(130, (1200 - 160 - (n - 1) * 18) // n)
        x0 = (1200 - (n * size + (n - 1) * 18)) // 2
        dr.rectangle((40, 450 + size - 6, 1160, 450 + size + 10), fill="#5B4636")
        for i, g in enumerate(LISTED):
            p = WORKSPACE / g["icon"]
            if p.exists():
                ic = rounded(Image.open(p), size)
                og.paste(ic, (x0 + i * (size + 18), 470 - 20), ic)
        og.save(A / "og.jpg", quality=86, optimize=True)


# ---------------------------------------------------------------- HTML

def stars_svg(seed=7, n=90):
    rnd = random.Random(seed)
    dots = []
    for _ in range(n):
        x, y = rnd.uniform(0, 1440), rnd.uniform(0, 520)
        r = rnd.choice([0.8, 0.8, 1, 1.2, 1.6])
        o = rnd.choice([0.35, 0.5, 0.7, 0.9])
        dots.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" opacity="{o}"/>')
    return ('<svg class="sky" viewBox="0 0 1440 640" preserveAspectRatio="xMidYMin slice" aria-hidden="true" focusable="false">'
            f'<g fill="#C9CDE6">{"".join(dots)}</g>'
            '<path class="mesa-far" d="M0 560 L120 548 L170 520 L300 520 L330 548 L520 556 L600 530 L640 504 L790 504 L820 530 L1000 548 L1080 540 L1110 512 L1230 512 L1262 540 L1440 552 L1440 640 L0 640Z"/>'
            '<path class="mesa-near" d="M0 600 L240 590 L420 598 L700 584 L980 596 L1200 588 L1440 596 L1440 640 L0 640Z"/>'
            '</svg>')


SPARK = ('<svg class="spark" viewBox="0 0 100 100" aria-hidden="true" focusable="false">'
         '<path d="M50 0 C54 36 64 46 100 50 C64 54 54 64 50 100 C46 64 36 54 0 50 C36 46 46 36 50 0Z"/></svg>')


def badge(g, cls=""):
    if g.get("app_store"):
        return (f'<a class="store-badge {cls}" href="{e(g["app_store"])}">'
                f'<img src="/assets/app-store-badge.svg" width="120" height="40" alt="Download {e(g["short"])} on the App Store"></a>')
    return f'<p class="soon {cls}">Coming soon to the App Store</p>'


def head(title, desc, path, og_image="/assets/og.jpg", extra=""):
    url = SITE + path
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#0F1229">
<link rel="icon" href="/assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/assets/icon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/lilita-one.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/nunito.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/site.css?v={VERSION}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{STUDIO}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{SITE}{og_image}">
{extra}</head>
"""


def header(current=""):
    def item(href, label, key):
        cur = ' aria-current="page"' if key == current else ""
        return f'<li><a href="{href}"{cur}>{label}</a></li>'
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="topbar">
  <div class="wrap topbar-in">
    <a class="brand" href="/"><img src="/assets/mark-96.webp" width="40" height="40" alt=""><span>{STUDIO}</span></a>
    <nav aria-label="Main"><ul>
      {item("/#games", "Games", "games")}
      {item("/#studio", "Studio", "studio")}
      {item("/support/", "Support", "support")}
    </ul></nav>
  </div>
</header>
"""


def footer():
    games = "".join(f'<li><a href="/{g["slug"]}/">{e(g["short"])}</a></li>' for g in LISTED)
    return f"""<footer class="footer">
  <div class="wrap footer-in">
    <div class="footer-brand">
      <img src="/assets/mark-96.webp" width="48" height="48" alt="">
      <p><strong>{LEGAL_NAME}</strong><br><a href="mailto:{CONTACT}">{CONTACT}</a></p>
    </div>
    <nav aria-label="Games"><h2>Games</h2><ul>{games}</ul></nav>
    <nav aria-label="Help"><h2>Help</h2><ul>
      <li><a href="/support/">Support and policies</a></li>
      <li><a href="mailto:{CONTACT}">Email support</a></li>
    </ul></nav>
  </div>
  <div class="wrap"><div class="footer-legal">
    <p>&copy; {YEAR} {LEGAL_NAME}. No cookies, trackers or analytics on this site.</p>
    <p>Apple and the Apple logo are trademarks of Apple Inc. App Store is a service mark of Apple Inc.</p>
  </div></div>
</footer>
"""


def doc(title, desc, path, body, current="", og_image="/assets/og.jpg", body_class=""):
    cls = f' class="{body_class}"' if body_class else ""
    return (head(title, desc, path, og_image) + f"<body{cls}>\n" + header(current)
            + f'<main id="main">\n{body}\n</main>\n' + footer() + "</body>\n</html>\n")


def shot_img(g, i, alt, w=430, h=932, lazy=True, sizes=""):
    load = ' loading="lazy" decoding="async"' if lazy else ""
    return f'<img src="/assets/games/{g["slug"]}/shot-{i}.webp" width="{w}" height="{h}" alt="{e(alt)}"{load}>'


def home():
    fence = "".join(
        f'<li style="--i:{i}"><a href="/{g["slug"]}/"><img src="/assets/games/{g["slug"]}/icon-160.webp" width="160" height="160" alt="{e(g["short"])}"></a></li>'
        for i, g in enumerate(LISTED))
    bands = []
    for g in LISTED:
        tags = "".join(f"<li>{e(t)}</li>" for t in g["tags"])
        shots = "".join(f"<li>{shot_img(g, i, alt)}</li>" for i, (_, alt) in enumerate(g["shots"][:3], 1))
        bands.append(f"""<article class="game" id="{g["slug"]}" style="--accent:{g["accent"]}">
  <div class="wrap game-in">
    <div class="game-text">
      <div class="game-head">
        <img class="game-icon" src="/assets/games/{g["slug"]}/icon-160.webp" width="160" height="160" alt="" loading="lazy">
        <div>
          <h3><a href="/{g["slug"]}/">{e(g["short"])}</a></h3>
          <p class="subtitle">{e(g["subtitle"])}</p>
        </div>
      </div>
      <p class="pitch">{e(g["pitch"])}</p>
      <ul class="tags" aria-label="Genre">{tags}</ul>
      <div class="game-actions">
        {badge(g)}
        <a class="more" href="/{g["slug"]}/">Screenshots and details<span class="visually-hidden"> for {e(g["short"])}</span></a>
      </div>
    </div>
    <ul class="phones" aria-label="{e(g["short"])} screenshots">{shots}</ul>
  </div>
</article>""")
    n = len(LISTED)
    count = {5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten"}.get(n, str(n))
    body = f"""<section class="hero" aria-labelledby="hero-title">
  {stars_svg()}
  <div class="wrap hero-in">
    {SPARK}
    <h1 id="hero-title">Small games with a western heart.</h1>
    <p class="lede">{STUDIO} makes original, feel-good games for iPhone: rodeo rides, ranches, gold mines and oil fields you can play a minute at a time.</p>
    <a class="button" href="#games">Meet the games</a>
  </div>
  <div class="fence-wrap wrap">
    <ul class="fence" aria-label="Our games">{fence}</ul>
  </div>
</section>

<section class="lineup" id="games" aria-labelledby="games-title">
  <div class="wrap section-head">
    <h2 id="games-title">The games</h2>
    <p>{count} games, all coming soon to the App Store.</p>
  </div>
  {"".join(bands)}
</section>

<section class="studio" id="studio" aria-labelledby="studio-title">
  <div class="wrap studio-in">
    <img src="/assets/logo-320.webp" width="320" height="320" alt="The Galileo Gaming logo: a gold telescope pointed at a bright star in a night sky" loading="lazy">
    <div>
      <h2 id="studio-title">About the studio</h2>
      <p>{STUDIO} is Martin Suarez, making small mobile games that respect your time. Every game is original, from the rules to the art, and most are about the rodeo, the ranch and the old West.</p>
      <p>They play offline, need no account and never make you wait on an energy timer. Ads keep them free, and one purchase in each game turns the between-screen ads off for good.</p>
    </div>
  </div>
</section>

<section class="contact" id="contact" aria-labelledby="contact-title">
  <div class="wrap contact-in">
    <h2 id="contact-title">Get in touch</h2>
    <p>Questions, bug reports or ideas: email <a href="mailto:{CONTACT}">{CONTACT}</a>. Tell us which game, your device and what happened, and we'll reply within a few days.</p>
  </div>
</section>"""
    return doc(f"{STUDIO}: small games with a western heart",
               f"{STUDIO} makes original, feel-good mobile games with a western and ranch heart: "
               + ", ".join(g["short"] for g in LISTED) + ".",
               "/", body, body_class="home")


def game_page(g):
    tags = "".join(f"<li>{e(t)}</li>" for t in g["tags"])
    feats = "".join(f"<li>{e(f)}</li>" for f in g["features"])
    gallery = "".join(f"<li>{shot_img(g, i, alt, lazy=i > 2)}</li>" for i, (_, alt) in enumerate(g["shots"], 1))
    others = "".join(
        f'<li><a href="/{o["slug"]}/"><img src="/assets/games/{o["slug"]}/icon-160.webp" width="160" height="160" alt="" loading="lazy"><span>{e(o["short"])}</span></a></li>'
        for o in LISTED if o is not g)
    body = f"""<section class="game-hero" style="--accent:{g["accent"]}" aria-labelledby="game-title">
  <div class="wrap game-hero-in">
    <img class="game-hero-icon" src="/assets/games/{g["slug"]}/icon-320.webp" width="320" height="320" alt="{e(g["short"])} app icon">
    <div>
      <h1 id="game-title">{e(g["short"])}</h1>
      <p class="subtitle">{e(g["subtitle"])}</p>
      <p class="pitch">{e(g["pitch"])}</p>
      <ul class="tags" aria-label="Genre">{tags}</ul>
      {badge(g)}
    </div>
  </div>
</section>

<section class="gallery" aria-labelledby="shots-title">
  <div class="wrap">
    <h2 id="shots-title" class="visually-hidden">Screenshots</h2>
    <ul class="shots" tabindex="0" aria-label="{e(g["short"])} screenshots, scroll sideways for more">{gallery}</ul>
  </div>
</section>

<section class="details">
  <div class="wrap details-in">
    <div>
      <h2>In the game</h2>
      <ul class="features">{feats}</ul>
    </div>
    <div class="help-box" style="--accent:{g["accent"]}">
      <h2>Help</h2>
      <ul>
        <li><a href="/{g["slug"]}/support">Support and FAQ</a></li>
        <li><a href="/{g["slug"]}/privacy">Privacy Policy</a></li>
        <li><a href="/{g["slug"]}/terms">Terms of Service</a></li>
        <li><a href="mailto:{CONTACT}">{CONTACT}</a></li>
      </ul>
    </div>
  </div>
</section>

<section class="others" aria-labelledby="others-title">
  <div class="wrap">
    <h2 id="others-title">More from {STUDIO}</h2>
    <ul class="other-games">{others}</ul>
  </div>
</section>"""
    return doc(f"{g['short']}: {g['subtitle']} | {STUDIO}", f"{g['name']}. {g['pitch']}",
               f"/{g['slug']}/", body, current="games", og_image=f"/assets/games/{g['slug']}/og.jpg",
               body_class="game-page")


def policy_doc(g, kind, title, inner):
    labels = [("support", "Support"), ("privacy", "Privacy Policy"), ("terms", "Terms of Service")]
    tabs = "".join(
        f'<li><a href="/{g["slug"]}/{k}"{" aria-current=page" if k == kind else ""}>{label}</a></li>' for k, label in labels)
    back = f'<a class="crumb" href="/{g["slug"]}/">{e(g["short"])}</a>' if g.get("listed", True) else f'<span class="crumb">{e(g["name"])}</span>'
    og = f"/assets/games/{g['slug']}/og.jpg" if g.get("listed", True) else "/assets/og.jpg"
    accent = g.get("accent", "#0F1229")
    body = f"""<div class="policy-bar" style="--accent:{accent}">
  <div class="wrap policy-bar-in">
    {back}
    <nav aria-label="{e(g["name"])} help pages"><ul>{tabs}</ul></nav>
  </div>
</div>
<article class="prose wrap">
{inner}
</article>"""
    return doc(title, f"{title}. {STUDIO}.", f"/{g['slug']}/{kind}", body, current="support", og_image=og,
               body_class="policy")


def support_index():
    rows = []
    for g in GAMES:
        name = (f'<a href="/{g["slug"]}/">{e(g["name"])}</a>' if g.get("listed", True) else e(g["name"]))
        icon = (f'<img src="/assets/games/{g["slug"]}/icon-160.webp" width="160" height="160" alt="" loading="lazy">'
                if g.get("icon") else '<span class="icon-blank" aria-hidden="true"></span>')
        rows.append(f"""<li>{icon}<div><h2>{name}</h2><ul class="links">
<li><a href="/{g["slug"]}/support">Support</a></li><li><a href="/{g["slug"]}/privacy">Privacy Policy</a></li><li><a href="/{g["slug"]}/terms">Terms of Service</a></li></ul></div></li>""")
    body = f"""<section class="page-head">
  <div class="wrap">
    <h1>Support and policies</h1>
    <p>Each game has its own support page, privacy policy and terms. For anything else, email <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>
  </div>
</section>
<div class="wrap"><ul class="support-list">{"".join(rows)}</ul></div>"""
    return doc(f"Support and policies | {STUDIO}", f"Support, privacy policies and terms for every {STUDIO} game.",
               "/support/", body, current="support")


def not_found():
    body = f"""<section class="page-head notfound">
  <div class="wrap">
    <h1>Page not found</h1>
    <p>There's no page at this address. It may have moved, or the link may have a typo.</p>
    <p><a class="button" href="/">Go to the home page</a> <a class="text-link" href="/support/">Support and policies</a></p>
  </div>
</section>"""
    return doc(f"Page not found | {STUDIO}", "This page doesn't exist.", "/404.html", body)


# ---------------------------------------------------------------- policy text (do not edit casually: legal copy)

def privacy(g):
    n = html.escape(g["name"])
    return policy_doc(g, "privacy", f"{g['name']} — Privacy Policy", f"""
<h1>{n} — Privacy Policy</h1>
<p class="date">Effective date: {EFFECTIVE}</p>
<h2>1. Overview</h2>
<p>{n} ("the Game") is developed by Martin Suarez (G4L1L3O G4M1N6). This policy explains what data the Game handles, how it is used, and your choices.</p>
<h2>2. Data stored on your device and in your Apple account</h2>
<ul><li><b>Save data:</b> game progress and settings, stored in a local file on your device. It is never sent to us.</li><li><b>iCloud sync (iOS):</b> if you are signed in to iCloud, a copy of your save is kept in your own iCloud account so progress carries over to your other devices and survives reinstalls. It is stored by Apple under your Apple Account; we cannot access it. You can turn this off in Settings → [your name] → iCloud.</li><li><b>Analytics ID:</b> if analytics is on (section 5a), a random ID created on this install, used only to count sessions and gameplay events. It is not your advertising ID or any other device identifier, and it is deleted when you turn Analytics off.</li><li><b>Game Center (iOS):</b> if you use Game Center, your scores and achievements are sent to Apple's Game Center under your Game Center profile, as described in <a href="https://www.apple.com/legal/privacy/">Apple's Privacy Policy</a>.</li></ul>
<h2>3. Data collected by third-party services</h2>
<ul>
<li><b>Google AdMob</b> (ads): may collect device identifiers, IP address, and ad interaction data to serve and measure ads. See <a href="https://policies.google.com/privacy">Google's Privacy Policy</a>.</li>
<li><b>GameAnalytics</b> (game analytics, processing on our behalf): receives the random analytics ID above, gameplay events (for example tutorial steps, rounds and scores, which optional ads you chose to watch, which in-app purchases you made and their price), your device model, operating-system version and game version, and your IP address, which it uses to determine your country. It does not receive your advertising ID, and the data is not used for advertising. GameAnalytics ApS processes this data under a data processing agreement and keeps raw data for up to 1 month and player statistics for up to 18 months; data may be processed in the United States under Standard Contractual Clauses. See <a href="https://gameanalytics.com/trust/privacy-notice">GameAnalytics' Privacy Notice</a>.</li>
<li><b>Apple App Store / StoreKit</b> and <b>Google Play Billing</b> (purchases): purchases are processed by Apple or Google. See <a href="https://www.apple.com/legal/privacy/">Apple's Privacy Policy</a> and <a href="https://policies.google.com/privacy">Google's Privacy Policy</a>.</li>
</ul>
<h2>4. Data we do not collect</h2>
<ul><li>No name, email, phone number, precise location, contacts, or account.</li><li>We run no servers that receive your data, and we do not sell your personal data. Data is shared with Google AdMob as described in section 5 and with GameAnalytics as described in sections 3 and 5a.</li></ul>
<h2>5. Advertising, tracking and your choices</h2>
<p>The Game shows ads from Google AdMob, including optional ads you choose to watch for in-game rewards. If you allow it, ads may be personalized using your device's advertising identifier and ad interaction data; this may be considered "sharing" for cross-context behavioral advertising under some US state laws.</p>
<ul>
<li><b>iOS:</b> the Game asks for your permission (App Tracking Transparency) before any cross-app tracking. If you decline, you still get the full game with non-personalized ads. You can change this at any time in Settings → Privacy &amp; Security → Tracking.</li>
<li><b>EU, UK and certain US states:</b> the Game shows a consent / privacy-choices form provided by Google before personalized ads are used. You can review or change your choices at any time from the Game's Settings → Privacy choices.</li>
<li><b>Android:</b> you can reset or delete your advertising ID and limit personalized ads in your device's Google settings.</li>
</ul>
<p>The optional "Remove Ads" purchase removes non-optional ads.</p>
<h2>5a. Analytics and your choices</h2>
<p>We use GameAnalytics to understand how the Game is played (for example where players get stuck) so we can improve it. This is not used for advertising or to track you across other apps.</p>
<ul>
<li><b>Everyone:</b> you can turn analytics off at any time in the Game's Settings → Analytics. Turning it off stops collection immediately and deletes the analytics ID and any unsent data from your device.</li>
<li><b>EU, UK and Switzerland:</b> analytics only runs if you agree to it in the consent form provided by Google (Settings → Privacy choices) or turn it on yourself in Settings → Analytics.</li>
</ul>
<h2>6. Children</h2>
<p>The Game is not directed at children under 13, and we do not knowingly collect personal information from children. If you believe a child has provided personal data, contact us and we will help remove it.</p>
<h2>7. Data retention and your rights</h2>
<p>Game data stays on your device until you delete the Game or its data. We hold no server-side data about you ourselves. Analytics data held by GameAnalytics on our behalf is keyed only to a random ID that we cannot link to you; turning Analytics off deletes that ID from your device, and GameAnalytics deletes the data on its retention schedule (raw data after 1 month, player statistics after up to 18 months). For other requests about analytics data, contact us. For data handled by Google or Apple, use their privacy tools.</p>
<h2>8. Changes</h2>
<p>We may update this policy; the effective date above shows the latest revision.</p>
<h2>9. Contact</h2>
<p>Questions? Email <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>
""")


def terms(g):
    n = html.escape(g["name"])
    return policy_doc(g, "terms", f"{g['name']} — Terms of Service", f"""
<h1>{n} — Terms of Service</h1>
<p class="date">Effective date: {EFFECTIVE}</p>
<h2>1. Acceptance</h2><p>By downloading, installing, or playing {n} ("the Game"), you agree to these Terms. If you do not agree, do not use the Game.</p>
<h2>2. License</h2><p>We grant you a limited, non-exclusive, non-transferable, revocable license to use the Game for personal, non-commercial entertainment on devices you own.</p>
<h2>3. In-app purchases</h2><p>The Game offers {html.escape(g["iap"])}. Purchases are final except where required by law or by the policies of the Apple App Store or Google Play. Virtual items have no real-world value.</p>
<h2>4. Conduct</h2><p>Do not modify, reverse-engineer, or decompile the Game, or tamper with save data or purchase verification.</p>
<h2>5. Save data</h2><p>Progress is stored on your device and, where available, synced through your iCloud account. We are not responsible for progress lost through device failure, uninstalling, or data corruption.</p>
<h2>6. Intellectual property</h2><p>The Game's content is owned by Martin Suarez or licensed from third-party creators (see the in-game Credits and Open-source licences screens).</p>
<h2>7. Disclaimer</h2><p>The Game is provided "as is", without warranties of any kind.</p>
<h2>8. Limitation of liability</h2><p>To the maximum extent permitted by law, we are not liable for indirect, incidental, special, consequential, or punitive damages arising from your use of the Game.</p>
<h2>9. Changes</h2><p>We may update these Terms; the effective date above shows the latest revision.</p>
<h2>10. Contact</h2><p>Questions? Email <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>
""")


def support(g):
    n = html.escape(g["name"])
    if g.get("cloud", True):
        sync = ("<p>Yes. When you are signed in to iCloud on your devices, the Game keeps your save in sync through iCloud automatically; "
                "if two devices disagree, the copy with more progress is kept. Game Center (leaderboards and achievements) is optional "
                "and signs you in quietly; it never blocks play. Make sure every device uses the same Apple Account and that iCloud is "
                "turned on in Settings &rarr; [your name] &rarr; iCloud.</p>")
    else:
        sync = ("<p>Not yet. Your progress is saved on this device only. Deleting the Game or moving to a new device without a "
                "device backup starts a new game.</p>")
    return policy_doc(g, "support", f"{g['name']} — Support", f"""
<h1>{n} — Support</h1>
<p>Need help with {n}? Email <a href="mailto:{CONTACT}">{CONTACT}</a> and tell us your device model, iOS version and what happened. We usually reply within a few days.</p>
<h2>How do I restore my purchases?</h2>
<p>Open the Game's Settings and tap <b>Restore Purchases</b>, signed in with the same Apple Account you bought with. Purchases such as Remove Ads come back on every device that uses that account.</p>
<h2>Does my progress sync between devices?</h2>
{sync}
<h2>How do I change my privacy choices?</h2>
<p>Ads in the Game come from Google AdMob. Where the law requires it, the Game's Settings shows <b>Privacy choices</b>, where you can review or change your ad consent at any time. On iOS you can also allow or stop app tracking in Settings &rarr; Privacy &amp; Security &rarr; Tracking. Gameplay analytics (GameAnalytics) can be turned off at any time in the Game's Settings &rarr; <b>Analytics</b>. See the <a href="/{g["slug"]}/privacy">Privacy Policy</a> for details.</p>
<h2>How do I delete my data?</h2>
<p>Deleting the Game removes its data from your device. If your save syncs through iCloud, that copy lives in your own iCloud account, not with us; resetting progress in the Game's Settings (where offered) also resets it. Game Center scores and achievements are managed by Apple in Settings &rarr; Game Center. Turning off Settings &rarr; Analytics deletes the random analytics ID and any unsent analytics data from your device; GameAnalytics deletes what it holds on its retention schedule. We keep no data about you on our own servers, so there is nothing else to delete; if you have questions, email us.</p>
<h2>Something else?</h2>
<p>Email <a href="mailto:{CONTACT}">{CONTACT}</a>. You can also read the <a href="/{g["slug"]}/terms">Terms of Service</a>.</p>
""")


# ---------------------------------------------------------------- write

VERSION = "1"


def main():
    global VERSION
    css = (ROOT / "assets" / "site.css").read_bytes()
    import hashlib
    VERSION = hashlib.sha1(css).hexdigest()[:8]
    build_images()
    urls = ["/", "/support/"]
    for g in GAMES:
        d = ROOT / g["slug"]
        d.mkdir(exist_ok=True)
        (d / "privacy.html").write_text(privacy(g))
        (d / "terms.html").write_text(terms(g))
        (d / "support.html").write_text(support(g))
        if g.get("listed", True):
            (d / "index.html").write_text(game_page(g))
            urls.append(f"/{g['slug']}/")
        urls += [f"/{g['slug']}/{k}" for k in ("support", "privacy", "terms")]
    (ROOT / "index.html").write_text(home())
    (ROOT / "support").mkdir(exist_ok=True)
    (ROOT / "support" / "index.html").write_text(support_index())
    (ROOT / "404.html").write_text(not_found())
    today = datetime.date.today().isoformat()
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    (ROOT / ".nojekyll").write_text("")
    print(f"built {len(urls)} pages")


if __name__ == "__main__":
    main()
