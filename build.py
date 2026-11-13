# -*- coding: utf-8 -*-
"""Génère le site statique Washie + flux produits.
Usage : python3 build.py [--out docs] [--skip-images]
Réglages : config.py
"""
import argparse, csv, html, json, os, re, shutil, unicodedata
from datetime import date
from xml.sax.saxutils import escape as xesc

import config as CFG
from catalog import BRAND, COLORS, PRODUCTS, SIZE_GUIDE, SIZE_W, ABS_SIZE
from images import product_svg, detail_svg, render

ap = argparse.ArgumentParser()
ap.add_argument("--out", default="docs")
ap.add_argument("--skip-images", action="store_true")
args = ap.parse_args()
BASE = CFG.SITE_URL.rstrip("/")
OUT = args.out
TODAY = date.today().isoformat()
FREE_SHIP, SHIP_PRICE = CFG.FREE_SHIPPING_FROM, CFG.SHIPPING_PRICE
E = html.escape


def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "standard"


def eur(v):
    return f"{v:,.2f} €".replace(",", " ").replace(".", ",")


def abs_url(path):
    return f"{BASE}/{path}" if path != "index.html" else BASE + "/"


def size_label(p, s):
    if not s:
        return ""
    if p.get("size_kind") == "kg":
        if p["id"] == "WS-BAIN":
            return {"S": "S (4–9 kg)", "M": "M (8–13 kg)", "L": "L (12–17 kg)"}[s]
        return f"{s} ({SIZE_W[s]})"
    if p.get("size_kind") == "abs":
        return f"{s} ({ABS_SIZE.get(s, 'pour couches M à XL')})" if not (p["id"] == "WS-JETABLE-20" and s == "T2") else "T2 (pour couches M à XL)"
    return s


# ---------------------------------------------------------------- variantes
for p in PRODUCTS:
    p["page"] = f"{p['slug']}.html"
    colors = p["colors"] or [""]
    sizes = p.get("sizes") or [""]
    p["variants"] = []
    for c in colors:
        for s in sizes:
            code = "-".join(x for x in [slugify(c)[:3].upper() if c else "", slugify(s).upper() if s else ""] if x)
            vid = f"{p['id']}-{code}" if code else p["id"]
            base = f"img/{p['slug']}-{slugify(c) if c else 'standard'}"
            p["variants"].append({"id": vid, "color": c, "size": s, "size_label": size_label(p, s), "image": base + ".png", "fiche": base + "-fiche.png"})
    p["image"] = p["variants"][0]["image"]
    p["final_price"] = p.get("sale_price") or p["price"]

# ---------------------------------------------------------------- dossiers
if os.path.exists(OUT):
    for f in os.listdir(OUT):
        fp = os.path.join(OUT, f)
        if f == "img" and args.skip_images:
            continue
        shutil.rmtree(fp) if os.path.isdir(fp) else os.remove(fp)
os.makedirs(f"{OUT}/img", exist_ok=True)
os.makedirs(f"{OUT}/feeds", exist_ok=True)

if not args.skip_images:
    done = set()
    for p in PRODUCTS:
        for v in p["variants"]:
            if v["image"] in done:
                continue
            done.add(v["image"])
            render(product_svg(p, v["color"]), f"{OUT}/{v['image']}")
            render(detail_svg(p, v["color"]), f"{OUT}/{v['fiche']}")
    hero = {"shape": "kit_big", "type": "", "name": "", "size": "", "highlights": []}
    render(product_svg(hero, "Sable"), f"{OUT}/img/og-washie.png", 1200)

# ---------------------------------------------------------------- contenus partagés
SYSTEMS = [
    ("Washie Classic", "Couche hybride : culotte douce + poche étanche intégrée. On glisse l'absorbant, c'est prêt.", "couche-lavable-hybride-washie-classic.html", "Débuter, crèche, nounou", "Aussi simple qu'une jetable"),
    ("Washie Switch", "Culotte + poche étanche détachable. On change la poche, on garde la culotte 2 à 3 changes.", "culotte-lavable-washie-switch.html", "Lavage fréquent, petit budget", "Moins de linge, séchage express"),
    ("Absorbant Jour", "Microfibre 3 épaisseurs à glisser dans la poche, pour 3 à 4 h.", "absorbants-lavables-jour-microfibre-lot-de-2.html", "Au quotidien", "Sèche très vite"),
    ("Absorbant Nuit", "4 épaisseurs pour 6 à 12 h, à combiner avec un booster si besoin.", "absorbant-lavable-nuit-sieste.html", "Nuit et longues siestes", "Bébé au sec toute la nuit"),
    ("Absorbant jetable", "Mode voyage : un absorbant jetable dans la même poche, rien à rapporter.", "absorbants-jetables-compostables-x20.html", "Vacances, sorties", "Hybride lavable / jetable"),
]

GLOBAL_FAQ = [
    ("Comment fonctionne une couche lavable hybride Washie ?",
     "Une couche Washie se compose d'une culotte douce, d'une poche étanche qui retient l'humidité et les selles, et d'un absorbant que l'on glisse dans la poche. L'absorbant peut être lavable (au quotidien) ou jetable (en voyage). Au change, on remplace l'absorbant ; si la poche n'est pas souillée, la couche peut être réutilisée."),
    ("Quelle différence entre Washie Classic et Washie Switch ?",
     "Sur la Classic, la poche étanche est intégrée à la culotte : c'est le système le plus simple, idéal pour débuter ou pour la crèche. Sur la Switch, la poche est détachable : à chaque change, on remplace seulement la poche et on garde la culotte 2 à 3 changes, ce qui réduit le linge et le budget."),
    ("Quelle taille de couche lavable choisir ?",
     "Les couches Washie existent en 5 tailles selon le poids : XS 2–4 kg, S 4–8 kg, M 6–12 kg, L 9–17 kg, XL 14–21 kg. Si votre bébé est entre deux tailles, prenez la plus grande : il la portera plus longtemps. Les absorbants suivent : T1 pour XS et S, T2 pour M et L, T3 pour XL."),
    ("Combien de couches lavables faut-il pour un bébé ?",
     "Pour un lavage tous les 2 jours avec Washie Classic : 6 à 7 couches et 12 à 14 absorbants en XS ou S, 5 à 6 couches et 10 à 12 absorbants en M, 4 à 5 couches et 10 à 12 absorbants en L. Avec Washie Switch : 2 à 4 culottes et 4 à 7 poches étanches selon la taille."),
    ("Comment laver les couches lavables Washie ?",
     "Stockez les couches au sec dans un sac ou un bac aéré, sans les faire tremper. Lavez la culotte et la poche à 40 °C, rabats fermés, et les absorbants jusqu'à 60 °C. N'utilisez ni adoucissant, ni javel, ni lessive avec agent de blanchiment ou azurant optique, qui abîment l'étanchéité. Séchez à l'air libre, sans sèche-linge ni fer à repasser pour les culottes et poches."),
    ("Peut-on utiliser les couches Washie la nuit ?",
     "Oui. Utilisez la couche dans la taille habituelle avec un absorbant Nuit & sieste (6 à 12 h selon les bébés) et ajoutez un booster pour les gros dormeurs. Pour les grands gabarits, la taille XL sert souvent de couche de nuit."),
    ("Les couches lavables sont-elles acceptées en crèche ?",
     "De plus en plus de crèches et d'assistantes maternelles acceptent les couches lavables. La Washie Classic s'utilise comme une jetable, ce qui facilite la prise en main par les professionnels. Fournissez un sac imperméable pour le retour des couches sales, et des absorbants jetables si la structure le préfère."),
    ("Quels sont les frais et délais de livraison ?",
     f"Livraison en France métropolitaine en 48 à 72 h ouvrées : {eur(SHIP_PRICE)}, offerte dès {eur(FREE_SHIP)} d'achat. Retours gratuits sous 30 jours pour les articles non utilisés."),
]

MERCHANT_RETURN = {"@type": "MerchantReturnPolicy", "applicableCountry": "FR",
                   "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
                   "merchantReturnDays": 30, "returnMethod": "https://schema.org/ReturnByMail",
                   "returnFees": "https://schema.org/FreeReturn"}


def shipping_details(price):
    return {"@type": "OfferShippingDetails",
            "shippingRate": {"@type": "MonetaryAmount", "value": 0 if price >= FREE_SHIP else SHIP_PRICE, "currency": "EUR"},
            "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "FR"},
            "deliveryTime": {"@type": "ShippingDeliveryTime",
                             "handlingTime": {"@type": "QuantitativeValue", "minValue": 0, "maxValue": 1, "unitCode": "DAY"},
                             "transitTime": {"@type": "QuantitativeValue", "minValue": 2, "maxValue": 3, "unitCode": "DAY"}}}


ORG = {"@context": "https://schema.org", "@type": "Organization", "name": BRAND, "url": BASE + "/",
       "logo": abs_url("img/og-washie.png"),
       "description": "Washie conçoit des couches lavables hybrides pour bébé : couche à poche étanche, culotte à poche détachable, absorbants lavables et jetables.",
       "slogan": "La couche lavable aussi simple qu'une jetable."}

LOGO = ('<svg viewBox="0 0 40 40" width="34" height="34" aria-hidden="true"><path d="M20 4c6 8 12 14 12 21a12 12 0 0 1-24 0C8 18 14 12 20 4z" fill="var(--sage)"/>'
        '<path d="M14 25c1.5 3 3.6 4.5 6 4.5s4.5-1.5 6-4.5" stroke="#fff" stroke-width="2.6" fill="none" stroke-linecap="round"/></svg>')

CFG_JS = json.dumps({"ga4": CFG.GA4_ID, "ads": CFG.GOOGLE_ADS_ID, "freeShip": FREE_SHIP, "ship": SHIP_PRICE,
                     "ordersOpen": CFG.ORDERS_OPEN, "leadEndpoint": CFG.LEAD_FORM_ENDPOINT})


def lead_form(source, title, text):
    if not CFG.LEAD_FORM_ENDPOINT:
        return ""
    return f'''<section class="wrap block"><form class="news" data-lead="{source}">
  <div><h2>{E(title)}</h2><p>{E(text)}</p></div>
  <div class="news-f"><label class="sr" for="em-{source}">E-mail</label><input id="em-{source}" type="email" placeholder="votre@email.fr" required><button class="btn">S'inscrire</button></div>
  <p class="form-msg" hidden></p></form></section>'''


def layout(title, desc, path, body, jsonld=(), og_image="img/og-washie.png", page_type="other", noindex=False):
    canon = abs_url(path)
    ld = "".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in jsonld)
    robots = "noindex,follow" if noindex else "index,follow,max-image-preview:large"
    return f'''<!DOCTYPE html>
<html lang="fr" data-page-type="{page_type}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="{robots}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{BRAND}"><meta property="og:locale" content="fr_FR">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{abs_url(og_image)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FBF8F2">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<script>window.WASHIE_CFG={CFG_JS};</script>
<script src="tracking.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,650&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
{ld}
</head>
<body>
<div class="demo">Livraison offerte dès {eur(FREE_SHIP)} · Retours gratuits 30 jours</div>
<header class="hdr">
  <div class="wrap hdr-in">
    <a class="logo" href="index.html" aria-label="Washie – accueil">{LOGO}<span>washie</span></a>
    <nav class="nav" aria-label="Navigation principale">
      <a href="boutique.html">Boutique</a>
      <a href="couche-lavable-hybride-washie-classic.html">Classic</a>
      <a href="culotte-lavable-washie-switch.html">Switch</a>
      <a href="boutique.html#absorbants">Absorbants</a>
      <a href="boutique.html#kits">Kits</a>
      <a href="guide-choisir-couche-lavable.html">Guide</a>
    </nav>
    <a class="cart-link" href="panier.html" aria-label="Panier"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M5 8h14l-1.2 11.2a2 2 0 0 1-2 1.8H8.2a2 2 0 0 1-2-1.8z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg><span id="cart-count">0</span></a>
  </div>
</header>
<main>
{body}
</main>
<footer class="ftr">
  <div class="wrap ftr-grid">
    <div><a class="logo" href="index.html">{LOGO}<span>washie</span></a>
      <p>Couches lavables hybrides pour bébé, de la naissance à la propreté. La couche lavable aussi simple qu'une jetable.</p></div>
    <div><h4>Boutique</h4><a href="couche-lavable-hybride-washie-classic.html">Washie Classic</a><a href="culotte-lavable-washie-switch.html">Washie Switch</a><a href="boutique.html#absorbants">Absorbants</a><a href="boutique.html#kits">Kits et packs</a><a href="boutique.html#accessoires">Accessoires</a></div>
    <div><h4>Conseils</h4><a href="guide-choisir-couche-lavable.html">Choisir sa couche lavable</a><a href="guide-des-tailles.html">Guide des tailles</a><a href="guide-entretien-couches-lavables.html">Laver ses couches</a><a href="faq.html">Questions fréquentes</a></div>
    <div><h4>Washie</h4><a href="a-propos.html">Notre histoire</a><a href="livraison-retours.html">Livraison & retours</a><a href="mentions-legales.html">Mentions légales</a><a href="confidentialite.html">Confidentialité & cookies</a><button class="linkbtn" onclick="washieShowConsent()">Gérer les cookies</button></div>
  </div>
  <p class="wrap legal">© {date.today().year} {BRAND}</p>
</footer>
<div class="cookie" id="cookie-banner" hidden role="dialog" aria-label="Cookies">
  <p>Nous utilisons des cookies de mesure d'audience et publicitaires (Google) pour comprendre comment vous arrivez sur Washie et améliorer le site. <a href="confidentialite.html">En savoir plus</a></p>
  <div><button class="btn ghost" onclick="washieConsent(false)">Refuser</button><button class="btn" onclick="washieConsent(true)">Accepter</button></div>
</div>
<script src="data.js"></script>
<script src="app.js"></script>
</body>
</html>'''


def card(p):
    sale = f'<s>{eur(p["price"])}</s> ' if p.get("sale_price") else ""
    badge = ('<span class="flag">Promo</span>' if p.get("sale_price") else
             '<span class="flag new">Nouveau</span>' if "nouveaute" in p["labels"] else
             '<span class="flag best">Best-seller</span>' if "bestseller" in p["labels"] else "")
    dots = "".join(f'<i style="background:{COLORS[c][0]}" title="{E(c)}"></i>' for c in p["colors"][:5]) if len(p["colors"]) > 1 else ""
    sizes = f'<span class="sizes">{" · ".join(p["sizes"])}</span>' if p.get("sizes") and p.get("size_kind") in ("kg", "abs") else ""
    return f'''<article class="card" data-pid="{p['id']}">
  <a href="{p['page']}" class="card-img">{badge}<img src="{p['image']}" alt="{E(p['name'])}" loading="lazy" width="500" height="500"></a>
  <div class="card-body">
    <span class="tag">{E(p['type'])}</span>
    <h3><a href="{p['page']}">{E(p['name'])}</a></h3>
    <p>{E(p['short'])}</p>
    <div class="card-foot"><span class="price">{sale}<b>{eur(p['final_price'])}</b></span><span class="dots">{dots}{sizes}</span></div>
  </div>
</article>'''


def grid(products, list_name):
    return f'<div class="grid" data-list="{list_name}">{"".join(card(p) for p in products)}</div>'


def faq_html(items):
    return "".join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in items)


def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": abs_url(u.split("#")[0])} for i, (n, u) in enumerate(items)]}


def crumbs_html(items):
    parts = [f'<a href="{u}">{E(n)}</a>' for n, u in items[:-1]] + [f'<span>{E(items[-1][0])}</span>']
    return '<nav class="crumbs wrap" aria-label="Fil d\'Ariane">' + " / ".join(parts) + "</nav>"


def size_table():
    rows = "".join(f'<tr><th>{s}</th><td>{w}</td><td>{a}</td><td>{"T1" if s in ("XS", "S") else ("T2" if s in ("M", "L") else "T3")}</td></tr>' for s, w, a in SIZE_GUIDE)
    return ('<div class="table-scroll"><table class="compare"><thead><tr><th>Taille</th><th>Poids</th><th>Âge indicatif</th><th>Absorbant</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')


def systems_table():
    rows = "".join(f'<tr><th><a href="{u}">{E(n)}</a></th><td>{E(d)}</td><td>{E(w)}</td><td>{E(b)}</td></tr>' for n, d, u, w, b in SYSTEMS)
    return ('<div class="table-scroll"><table class="compare"><thead><tr><th>Élément</th><th>Principe</th><th>Idéal pour</th><th>Point fort</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')


pages = {}
by_range = lambda r: [p for p in PRODUCTS if p["range"] == r]
pid = {p["id"]: p for p in PRODUCTS}

# ---------------------------------------------------------------- ACCUEIL
best = [pid[i] for i in ("WS-CLASSIC", "WS-SWITCH", "WS-KIT-CLASSIC", "WS-PACK-CLASSIC", "WS-ABS-JOUR", "WS-ABS-NUIT", "WS-POCHE", "WS-JETABLE-20")]
home_body = f'''
<section class="hero">
  <div class="wrap hero-in">
    <div>
      <p class="eyebrow">Couches lavables hybrides</p>
      <h1>La couche lavable aussi simple qu'une jetable.</h1>
      <p class="lead">Une culotte douce, une poche étanche, un absorbant lavable ou jetable : Washie rend le lavable facile, de la naissance à la propreté, en 5 tailles ajustées.</p>
      <div class="cta"><a class="btn" href="boutique.html" data-cta="hero_shop">Découvrir la gamme</a><a class="btn ghost" href="kit-essai-couche-lavable-washie-classic.html" data-cta="hero_trial_kit">Kit d'essai à {eur(39)}</a></div>
      <ul class="trust"><li>Livraison offerte dès {eur(FREE_SHIP)}</li><li>Retours gratuits 30 jours</li><li>5 tailles de 2 à 21 kg</li></ul>
    </div>
    <img src="img/og-washie.png" alt="Couches lavables Washie en différentes couleurs avec absorbant" width="600" height="600">
  </div>
</section>
<section class="wrap block">
  <div class="sec-head"><h2>Comment ça marche</h2><a href="guide-choisir-couche-lavable.html" data-cta="home_guide">Le guide complet →</a></div>
  <div class="steps3">
    <div class="step"><b>1</b><h3>Glissez l'absorbant</h3><p>Dans la poche étanche : lavable au quotidien, jetable en voyage.</p></div>
    <div class="step"><b>2</b><h3>Fermez, c'est prêt</h3><p>Rabats doux, élastiques aux cuisses : ça se met comme une jetable.</p></div>
    <div class="step"><b>3</b><h3>Changez l'absorbant</h3><p>La couche ou la culotte Switch resservent ; tout se lave à 40–60 °C.</p></div>
  </div>
</section>
<section class="wrap block">
  <div class="sec-head"><h2>Les plus choisis</h2><a href="boutique.html" data-cta="home_all_products">Tout voir →</a></div>
  {grid(best, "home_bestsellers")}
</section>
<section class="band">
  <div class="wrap split">
    <div><h2>Classic ou Switch ?</h2>
      <p><b>Washie Classic</b> : la poche étanche est intégrée. Le plus simple, parfait pour débuter et pour la crèche.</p>
      <p><b>Washie Switch</b> : la poche se détache. On change la poche, on garde la culotte 2 à 3 changes : moins de linge, moins de budget.</p>
      <p>Les deux utilisent les mêmes absorbants Washie (Jour, Nuit, coton bio, jetables).</p>
      <a class="btn" href="guide-choisir-couche-lavable.html" data-cta="home_compare_guide">Comparer en détail</a></div>
    <div>{systems_table()}</div>
  </div>
</section>
<section class="wrap block narrow">
  <h2>Quelle taille pour mon bébé ?</h2>
  {size_table()}
  <p><a href="guide-des-tailles.html" data-cta="home_size_guide">Guide des tailles complet →</a></p>
</section>
<section class="wrap block narrow">
  <h2>Questions fréquentes</h2>
  <div class="faq">{faq_html(GLOBAL_FAQ[:5])}</div>
  <p><a href="faq.html">Toutes les questions →</a></p>
</section>
{lead_form("home_newsletter", "Bien démarrer avec le lavable", "Un e-mail par semaine pendant un mois : tailles, lavage, nuit, crèche.")}'''
itemlist = {"@context": "https://schema.org", "@type": "ItemList", "name": "Couches lavables Washie",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": abs_url(p["page"]), "name": p["name"]} for i, p in enumerate(PRODUCTS)]}
website = {"@context": "https://schema.org", "@type": "WebSite", "name": BRAND, "url": BASE + "/", "inLanguage": "fr-FR"}
pages["index.html"] = layout(
    "Washie – Couches lavables hybrides pour bébé, aussi simples qu'une jetable",
    "Couches lavables hybrides Washie : culotte douce + poche étanche + absorbant lavable ou jetable. 5 tailles de 2 à 21 kg. Kit d'essai, packs, livraison offerte dès 49 €.",
    "index.html", home_body, [ORG, website, itemlist, faq_ld(GLOBAL_FAQ[:5])], page_type="home")

# ---------------------------------------------------------------- BOUTIQUE
sections = [("couches", "Couches et culottes", "Couches"), ("absorbants", "Absorbants et boosters", "Absorbants"),
            ("kits", "Kits d'essai et packs", "Kits"), ("accessoires", "Accessoires", "Accessoires"), ("entretien", "Entretien", "Entretien")]
chips = '<button class="chip on" data-filter="all">Tout</button>' + "".join(f'<button class="chip" data-filter="{a}">{E(t)}</button>' for a, t, r in sections)
shop_secs = "".join(f'<section id="{a}" class="shop-sec" data-range="{a}"><h2>{E(t)}</h2>{grid(by_range(r), "shop_" + a)}</section>' for a, t, r in sections)
shop_cr = [("Accueil", "index.html"), ("Boutique", "boutique.html")]
pages["boutique.html"] = layout(
    "Boutique couches lavables hybrides : couches, absorbants, kits | Washie",
    "Toute la gamme Washie : couche hybride Classic, culotte Switch à poche détachable, absorbants lavables jour, nuit et coton bio, absorbants jetables, kits d'essai et packs.",
    "boutique.html", f'''{crumbs_html(shop_cr)}
<section class="wrap block">
  <h1>Toute la gamme Washie</h1>
  <p class="lead">{len(PRODUCTS)} produits pour équiper bébé de 2 à 21 kg : couches hybrides, culottes à poche détachable, absorbants lavables et jetables, kits, bain, apprentissage et entretien.</p>
  <div class="chips" role="toolbar" aria-label="Filtrer par gamme">{chips}</div>
  {shop_secs}
</section>''', [itemlist, crumbs_ld(shop_cr)], page_type="plp")

# ---------------------------------------------------------------- PAGES PRODUIT
CARE = {
    "Couches": "Stockez au sec, sans trempage. Culotte et poche : lavage 40 °C, rabats fermés, séchage à l'air libre, sans sèche-linge ni fer. Évitez adoucissant, javel, solvants, et lessives avec agent de blanchiment, azurant optique ou plus de 5 % de parfum : ils abîment l'étanchéité.",
    "Absorbants": "Lavage jusqu'à 60 °C. Séchage à l'air libre ou sèche-linge basse température. Prélavez les absorbants neufs avant la première utilisation.",
}
REL = {"Couches": ["WS-ABS-JOUR", "WS-ABS-NUIT", "WS-VOILES-100", "WS-SAC"],
       "Absorbants": ["WS-CLASSIC", "WS-SWITCH", "WS-BOOSTER", "WS-LESSIVE"],
       "Kits": ["WS-ABS-JOUR", "WS-VOILES-100", "WS-SAC", "WS-LESSIVE"]}
RANGE_ANCHOR = {r: a for a, t, r in sections}


def product_page(p):
    v0 = p["variants"][0]
    swatches = ""
    if len(p["colors"]) > 1:
        swatches = ('<div class="opt"><span class="opt-l">Couleur : <b id="color-name">' + E(p["colors"][0]) + '</b></span><div class="swatches">' +
                    "".join(f'<button type="button" class="sw{" on" if i == 0 else ""}" data-color="{E(c)}" style="--c:{COLORS[c][0]}" aria-label="{E(c)}"></button>' for i, c in enumerate(p["colors"])) + "</div></div>")
    elif p["colors"]:
        swatches = f'<div class="opt"><span class="opt-l">Couleur : <b>{E(p["colors"][0])}</b></span></div>'
    sizes = ""
    if p.get("sizes"):
        default = "M" if "M" in p["sizes"] else p["sizes"][0]
        sizes = ('<div class="opt"><label class="opt-l" for="size">Taille</label><select id="size">' +
                 "".join(f'<option value="{E(s)}"{" selected" if s == default else ""}>{E(size_label(p, s))}</option>' for s in p["sizes"]) + "</select>")
        if p.get("size_kind") in ("kg", "abs"):
            sizes += f'<details class="sg" data-size-guide><summary>Guide des tailles</summary>{size_table()}<p><small>Entre deux tailles, prenez la plus grande.</small></p></details>'
        sizes += "</div>"
    price_html = (f'<s>{eur(p["price"])}</s> <b>{eur(p["sale_price"])}</b> <span class="save">−{round(100 - p["sale_price"] / p["price"] * 100)} %</span>'
                  if p.get("sale_price") else f'<b>{eur(p["price"])}</b>')
    attrs = "".join(f'<tr><th>{E(k)}</th><td>{E(v)}</td></tr>' for k, v in p["attrs"].items())
    hl = "".join(f'<li>{E(h)}</li>' for h in p["highlights"])
    thumbs = "".join(f'<button type="button" class="th"><img src="{x}" alt="" width="90" height="90"></button>' for x in [v0["image"], v0["fiche"]])
    related = [pid[i] for i in REL.get(p["range"], ["WS-CLASSIC", "WS-KIT-CLASSIC", "WS-ABS-JOUR", "WS-LESSIVE"]) if i != p["id"]][:4]
    faq_items = p["faq"] + [GLOBAL_FAQ[4]]
    care = CARE.get(p["range"], "Voir la notice fournie avec le produit.")
    crumbs = [("Accueil", "index.html"), ("Boutique", "boutique.html"), (p["range"], f"boutique.html#{RANGE_ANCHOR[p['range']]}"), (p["name"], p["page"])]

    def offer(v):
        return {"@type": "Offer", "url": abs_url(p["page"]) + (f"?variant={v['id']}" if len(p["variants"]) > 1 else ""),
                "priceCurrency": "EUR", "price": f"{p['final_price']:.2f}",
                "availability": "https://schema.org/PreOrder" if not CFG.ORDERS_OPEN else "https://schema.org/InStock",
                "itemCondition": "https://schema.org/NewCondition", "priceValidUntil": f"{date.today().year + 1}-12-31",
                "shippingDetails": shipping_details(p["final_price"]), "hasMerchantReturnPolicy": MERCHANT_RETURN}

    def prod_ld(v, ctx=True):
        nm = p["name"] + (f" – {v['color']}" if v["color"] and len(p["colors"]) > 1 else "") + (f" – Taille {v['size']}" if v["size"] else "")
        d = {"@type": "Product", "name": nm, "sku": v["id"], "mpn": v["id"], "image": [abs_url(v["image"]), abs_url(v["fiche"])],
             "description": p["description"], "brand": {"@type": "Brand", "name": BRAND},
             "material": p["material"] or None, "color": v["color"] or None, "size": v["size_label"] or p["size"],
             "category": p["product_type"], "offers": offer(v),
             "additionalProperty": [{"@type": "PropertyValue", "name": k, "value": val} for k, val in p["attrs"].items()]}
        if ctx:
            d["@context"] = "https://schema.org"
        return {k: val for k, val in d.items() if val is not None}

    if len(p["variants"]) > 1:
        varies = (["https://schema.org/color"] if len(p["colors"]) > 1 else []) + (["https://schema.org/size"] if p.get("sizes") else [])
        ld = {"@context": "https://schema.org", "@type": "ProductGroup", "name": p["name"], "productGroupID": p["id"],
              "description": p["description"], "brand": {"@type": "Brand", "name": BRAND}, "url": abs_url(p["page"]),
              "variesBy": varies, "hasVariant": [prod_ld(v, False) for v in p["variants"]]}
    else:
        ld = prod_ld(v0)
    ship_txt = "Livraison offerte" if p["final_price"] >= FREE_SHIP else f"Livraison {eur(SHIP_PRICE)}, offerte dès {eur(FREE_SHIP)}"
    body = f'''{crumbs_html(crumbs)}
<section class="wrap pdp" data-product="{p['id']}">
  <div class="gallery">
    <img id="main-img" src="{v0['image']}" alt="{E(p['name'])}" width="700" height="700">
    <div class="thumbs" id="thumbs">{thumbs}</div>
  </div>
  <div class="buy">
    <span class="tag">{E(p['type'])}</span>
    <h1>{E(p['name'])}</h1>
    <p class="pdp-price">{price_html}</p>
    <p class="lead">{E(p['short'])}</p>
    {swatches}{sizes}
    <div class="add"><label class="sr" for="qty">Quantité</label><input id="qty" type="number" min="1" max="50" value="1"><button class="btn" id="add-btn">Ajouter au panier</button></div>
    <p class="added" id="added" hidden>Ajouté au panier · <a href="panier.html">Voir le panier</a></p>
    <ul class="hl">{hl}</ul>
    <ul class="reassure"><li>{ship_txt}</li><li>Retours gratuits 30 jours</li><li>Réf. <span id="sku">{v0['id']}</span></li></ul>
  </div>
</section>
<section class="wrap pdp-info">
  <div><h2>Description</h2><p>{E(p['description'])}</p><h2>Entretien</h2><p>{E(care)}</p></div>
  <div><h2>Caractéristiques</h2><table class="spec"><tbody>{attrs}<tr><th>Marque</th><td>{BRAND}</td></tr></tbody></table></div>
</section>
<section class="wrap block narrow"><h2>Questions sur ce produit</h2><div class="faq">{faq_html(faq_items)}</div></section>
<section class="wrap block"><div class="sec-head"><h2>Souvent achetés avec</h2></div>{grid(related, "pdp_related")}</section>'''
    return layout(f"{p['name']} – {eur(p['final_price'])} | {BRAND}", p["short"][:155], p["page"], body,
                  [ld, crumbs_ld(crumbs), faq_ld(faq_items)], og_image=v0["image"], page_type="pdp")


for p in PRODUCTS:
    pages[p["page"]] = product_page(p)

# ---------------------------------------------------------------- GUIDES


def article(path, title, desc, h1, content, crumbs_name):
    crumbs = [("Accueil", "index.html"), ("Conseils", "guide-choisir-couche-lavable.html"), (crumbs_name, path)]
    art = {"@context": "https://schema.org", "@type": "Article", "headline": h1, "description": desc, "inLanguage": "fr-FR",
           "datePublished": TODAY, "dateModified": TODAY, "author": {"@type": "Organization", "name": BRAND},
           "publisher": {"@type": "Organization", "name": BRAND, "logo": {"@type": "ImageObject", "url": abs_url("img/og-washie.png")}},
           "mainEntityOfPage": abs_url(path), "image": abs_url("img/og-washie.png")}
    pages[path] = layout(title, desc, path, f'{crumbs_html(crumbs)}<article class="wrap block prose"><h1>{E(h1)}</h1>{content}</article>',
                         [art, crumbs_ld(crumbs)], page_type="guide")


article("guide-choisir-couche-lavable.html",
        "Quelle couche lavable choisir ? Hybride, TE1, TE2 : le guide | Washie",
        "Comment choisir sa couche lavable : systèmes (TE1, TE2, hybride, préformée), tailles, quantités, budget, et différences entre Washie Classic et Switch.",
        "Quelle couche lavable choisir ? Le guide pour bien démarrer",
        f'''<p class="lead">En bref : si vous débutez ou confiez bébé à une crèche, choisissez une couche simple à poser comme la <a href="couche-lavable-hybride-washie-classic.html">Washie Classic</a>. Si vous lavez souvent et voulez limiter le linge et le budget, un système à poche détachable comme la <a href="culotte-lavable-washie-switch.html">Washie Switch</a> est plus économique. Pour la nuit, ajoutez un absorbant renforcé.</p>
<h2>Les grands systèmes de couches lavables</h2>
<ul><li><b>TE1 (tout-en-un)</b> : une seule pièce, absorbant cousu. Simple, mais long à sécher.</li>
<li><b>TE2 (tout-en-deux)</b> : culotte imperméable + absorbant amovible. Économique, séchage rapide.</li>
<li><b>Hybride</b> : culotte + poche étanche + absorbant lavable <i>ou</i> jetable. Coupe fine et souplesse en déplacement. C'est le principe des couches Washie.</li>
<li><b>Préformée ou lange + culotte de protection</b> : le moins cher, mais demande un peu de technique.</li></ul>
<h2>Washie Classic ou Washie Switch ?</h2>{systems_table()}
<h2>Quelle taille ?</h2>{size_table()}<p>Entre deux tailles, prenez la plus grande. <a href="guide-des-tailles.html">Voir le guide des tailles</a>.</p>
<h2>Combien en acheter ?</h2>
<table class="spec"><tbody><tr><th>Classic, taille XS ou S</th><td>6 à 7 couches + 12 à 14 absorbants T1</td></tr><tr><th>Classic, taille M</th><td>5 à 6 couches + 10 à 12 absorbants T2</td></tr><tr><th>Classic, taille L</th><td>4 à 5 couches + 10 à 12 absorbants T2</td></tr><tr><th>Switch, taille S</th><td>3 à 4 culottes + 6 à 7 poches + 12 à 14 absorbants T1</td></tr><tr><th>Switch, taille M ou L</th><td>2 à 3 culottes + 4 à 6 poches + 10 à 12 absorbants T2</td></tr></tbody></table>
<p><small>Base : lavage tous les 2 jours, usage à temps plein.</small></p>
<h2>Quel budget ?</h2>
<p>Comptez environ 260 à 300 € par taille pour un équipement à temps plein (par exemple le <a href="pack-equipement-couches-lavables-washie-classic.html">pack équipement Classic</a>). Le <a href="kit-essai-couche-lavable-washie-classic.html">kit d'essai</a> permet de tester pour {eur(39)} avant d'investir.</p>
<h2>Bien démarrer en 3 étapes</h2><ol><li>Testez avec un kit d'essai dans la taille actuelle de bébé.</li><li>Commencez à mi-temps, à la maison, en journée.</li><li>Équipez-vous à temps plein, puis ajoutez la nuit avec l'absorbant Nuit.</li></ol>
<div class="faq">{faq_html(GLOBAL_FAQ[:4])}</div>''', "Choisir sa couche lavable")

article("guide-des-tailles.html",
        "Guide des tailles couches lavables Washie (XS à XL, 2 à 21 kg) | Washie",
        "Quelle taille de couche lavable choisir ? Tableau des tailles Washie XS, S, M, L, XL par poids et âge, absorbants T1, T2, T3 et conseils d'ajustement.",
        "Guide des tailles des couches lavables Washie",
        f'''<p class="lead">Les couches Washie existent en 5 tailles selon le poids de bébé, de 2 à 21 kg. Les absorbants existent en 3 tailles (T1, T2, T3) qui correspondent aux couches.</p>
{size_table()}
<h2>Comment savoir si la taille est bonne ?</h2>
<ul><li>Les élastiques des cuisses sont dans le pli de l'aine, sans marquer la peau.</li><li>La poche étanche couvre bien les fesses ; le côté le plus large est à l'arrière (tailles M à XL).</li><li>Les rabats ferment sans tirer, avec un doigt de marge au ventre.</li></ul>
<h2>Entre deux tailles ?</h2><p>Prenez la plus grande : votre enfant la portera plus longtemps. Si des fuites apparaissent aux cuisses avec une couche trop grande, resserrez les rabats ou repassez temporairement à la taille inférieure.</p>
<h2>Correspondance des absorbants</h2><table class="spec"><tbody><tr><th>T1</th><td>Couches XS et S</td></tr><tr><th>T2</th><td>Couches M et L</td></tr><tr><th>T3</th><td>Couches XL</td></tr></tbody></table>''', "Guide des tailles")

article("guide-entretien-couches-lavables.html",
        "Comment laver les couches lavables ? La routine simple | Washie",
        "Routine de lavage des couches lavables hybrides : stockage, températures (40 °C culottes, 60 °C absorbants), lessive adaptée, séchage, et solutions aux fuites et odeurs.",
        "Comment laver les couches lavables : la routine simple",
        '''<p class="lead">En bref : stockage au sec sans trempage, culottes et poches à 40 °C rabats fermés, absorbants jusqu'à 60 °C, lessive sans adoucissant ni agent de blanchiment, séchage à l'air libre.</p>
<ol class="steps"><li><b>Au change</b> : jetez le voile et les selles aux toilettes. Retirez l'absorbant de la poche.</li>
<li><b>Stockage</b> : au sec, dans un sac imperméable ou un bac aéré. Pas de trempage : il abîme l'étanchéité.</li>
<li><b>Lavage</b> : tous les 2 jours. Culottes et poches à 40 °C, rabats fermés. Absorbants jusqu'à 60 °C (en même temps à 40 °C si vous préférez une seule machine, avec un rinçage supplémentaire).</li>
<li><b>Lessive</b> : sans adoucissant, javel, solvant, agent de blanchiment, azurant optique, ni plus de 5 % de parfum.</li>
<li><b>Séchage</b> : à l'air libre. Pas de sèche-linge ni de fer pour les culottes et poches ; sèche-linge basse température possible pour les absorbants.</li></ol>
<h2>Fuites ou odeurs ? Les causes fréquentes</h2>
<table class="spec"><tbody><tr><th>Fuites aux cuisses</th><td>Taille inadaptée ou élastiques pas dans le pli de l'aine. Vérifiez le <a href="guide-des-tailles.html">guide des tailles</a>.</td></tr><tr><th>Absorbant saturé</th><td>Changez plus souvent, passez à l'absorbant Nuit ou ajoutez un <a href="boosters-microfibre-duo.html">booster</a>.</td></tr><tr><th>Poche qui laisse passer</th><td>Lessive ou produit agressif (javel, adoucissant, solvant) : changez de lessive.</td></tr><tr><th>Odeur d'ammoniaque</th><td>Lessive sous-dosée ou rinçage insuffisant : augmentez la dose et ajoutez un rinçage.</td></tr></tbody></table>
<p>La <a href="lessive-speciale-couches-lavables.html">lessive Washie</a> est formulée pour préserver poches et absorbants.</p>''', "Laver ses couches")

# ---------------------------------------------------------------- FAQ & pages info
faq_cr = [("Accueil", "index.html"), ("FAQ", "faq.html")]
pages["faq.html"] = layout("FAQ couches lavables hybrides : vos questions | Washie",
                           "Fonctionnement, Classic ou Switch, tailles, quantités, lavage, nuit, crèche, livraison : toutes les réponses sur les couches lavables Washie.",
                           "faq.html", f'{crumbs_html(faq_cr)}<section class="wrap block narrow"><h1>Questions fréquentes</h1><div class="faq">{faq_html(GLOBAL_FAQ)}</div></section>',
                           [faq_ld(GLOBAL_FAQ), crumbs_ld(faq_cr)], page_type="faq")

L = CFG.LEGAL
info = {
    "a-propos.html": ("Notre histoire", "Washie conçoit des couches lavables hybrides pensées pour être aussi simples qu'une jetable.",
        "<p>Washie est née d'un constat simple : beaucoup de parents veulent passer aux couches lavables, mais renoncent face à la complexité des systèmes, des pliages et des quantités. Nous avons conçu une gamme courte et cohérente autour d'un principe hybride : une culotte douce, une poche étanche, un absorbant lavable ou jetable.</p><p>Deux systèmes – <a href='couche-lavable-hybride-washie-classic.html'>Classic</a> et <a href='culotte-lavable-washie-switch.html'>Switch</a> –, cinq tailles de 2 à 21 kg, et des absorbants communs pour le jour, la nuit et les déplacements.</p>", "about"),
    "livraison-retours.html": ("Livraison et retours", f"Livraison en France métropolitaine {eur(SHIP_PRICE)}, offerte dès {eur(FREE_SHIP)}. Retours gratuits sous 30 jours.",
        f"<table class='spec'><tbody><tr><th>Zone</th><td>France métropolitaine</td></tr><tr><th>Tarif</th><td>{eur(SHIP_PRICE)} — offerte dès {eur(FREE_SHIP)}</td></tr><tr><th>Préparation</th><td>Sous 24 h ouvrées</td></tr><tr><th>Délai</th><td>48 à 72 h ouvrées</td></tr><tr><th>Retours</th><td>30 jours, gratuits, articles non utilisés et non lavés</td></tr></tbody></table>", "info"),
    "mentions-legales.html": ("Mentions légales", "Mentions légales du site Washie.",
        f"<table class='spec'><tbody><tr><th>Éditeur</th><td>{E(L['company'])}</td></tr><tr><th>Adresse</th><td>{E(L['address'])}</td></tr><tr><th>SIREN</th><td>{E(L['siren'])}</td></tr><tr><th>TVA</th><td>{E(L['vat'])}</td></tr><tr><th>Directeur·rice de la publication</th><td>{E(L['director'])}</td></tr><tr><th>Contact</th><td>{E(L['email'])}</td></tr><tr><th>Hébergeur</th><td>{E(L['host'])}</td></tr></tbody></table>", "info"),
    "confidentialite.html": ("Confidentialité et cookies", "Comment Washie utilise les cookies de mesure d'audience et publicitaires.",
        "<p>Avec votre accord, nous utilisons <b>Google Analytics 4</b> pour mesurer l'audience (pages vues, parcours, provenance des visites : moteur de recherche, publicité, réseaux sociaux, assistants IA…) et, le cas échéant, <b>Google Ads</b> pour mesurer l'efficacité de nos campagnes. Sans votre accord, aucun cookie de mesure ou publicitaire n'est déposé ; Google peut recevoir des signaux anonymes sans cookie (mode consentement).</p><p>Votre panier est conservé uniquement dans votre navigateur. Vous pouvez modifier votre choix à tout moment via le lien « Gérer les cookies » en bas de page. Durée de conservation des données Analytics : 14 mois.</p>", "info"),
}
for path, (t, d, c, ptype) in info.items():
    cr = [("Accueil", "index.html"), (t, path)]
    pages[path] = layout(f"{t} | {BRAND}", d, path, f'{crumbs_html(cr)}<section class="wrap block prose"><h1>{E(t)}</h1>{c}</section>',
                         [crumbs_ld(cr)], page_type=ptype, noindex=path in ("mentions-legales.html", "confidentialite.html"))

prelaunch = "" if CFG.ORDERS_OPEN else f'''<div class="modal" id="prelaunch-modal" hidden><div class="modal-box"><h2>Les commandes ouvrent très bientôt</h2>
<p>Washie finalise sa première production. Votre panier reste enregistré sur cet appareil.</p>{lead_form("prelaunch_waitlist", "Être prévenu·e de l'ouverture", "Recevez un e-mail le jour du lancement.").replace('class="wrap block"', '')}
<button class="btn" id="close-modal">Continuer mes achats</button></div></div>'''
pages["panier.html"] = layout(f"Panier | {BRAND}", "Votre panier Washie.", "panier.html",
                              f'<section class="wrap block narrow"><h1>Votre panier</h1><div id="cart"></div>{prelaunch}</section>', page_type="cart", noindex=True)

for name, content in pages.items():
    with open(f"{OUT}/{name}", "w", encoding="utf-8") as f:
        f.write(content)

data = {p["id"]: {"name": p["name"], "page": p["page"], "price": p["final_price"], "list_price": p["price"], "type": p["type"], "range": p["range"],
                  "variants": [{k: v[k] for k in ("id", "color", "size", "image", "fiche")} for v in p["variants"]]} for p in PRODUCTS}
with open(f"{OUT}/data.js", "w", encoding="utf-8") as f:
    f.write("window.WS_PRODUCTS=" + json.dumps(data, ensure_ascii=False) + ";")
for a in ("app.js", "style.css", "tracking.js"):
    shutil.copy(f"assets/{a}", f"{OUT}/{a}")
with open(f"{OUT}/favicon.svg", "w") as f:
    f.write(LOGO.replace('width="34" height="34" aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"').replace("var(--sage)", "#7E9A7B"))
open(f"{OUT}/.nojekyll", "w").close()

# ---------------------------------------------------------------- FLUX PRODUITS
avail = "in_stock" if CFG.ORDERS_OPEN else "preorder"
rows = []
for p in PRODUCTS:
    multi = len(p["variants"]) > 1
    for v in p["variants"]:
        bits = [p["name"]] + ([v["color"]] if v["color"] and len(p["colors"]) > 1 else []) + ([f"Taille {v['size_label']}"] if v["size"] else [])
        fp = p["final_price"]
        rows.append({
            "id": v["id"], "item_group_id": p["id"] if multi else "",
            "title": " – ".join(bits)[:150], "description": p["description"], "short_description": p["short"],
            "link": abs_url(p["page"]) + (f"?variant={v['id']}" if multi else ""),
            "image_link": abs_url(v["image"]), "additional_image_link": abs_url(v["fiche"]),
            "availability": avail, "availability_date": "" if CFG.ORDERS_OPEN else f"{CFG.LAUNCH_DATE}T00:00:00+01:00",
            "price": f"{p['price']:.2f} EUR", "sale_price": f"{p['sale_price']:.2f} EUR" if p.get("sale_price") else "",
            "brand": BRAND, "mpn": v["id"], "identifier_exists": "no", "condition": "new",
            "google_product_category": p["gcat"], "product_type": p["product_type"],
            "color": v["color"], "size": v["size_label"] or p["size"], "size_system": "FR" if v["size"] else "",
            "material": p["material"], "age_group": p["age_group"], "gender": "unisex" if p["age_group"] else "",
            "product_highlight": p["highlights"], "product_detail": [("Caractéristiques", k, val) for k, val in p["attrs"].items()],
            "shipping": f"FR:::{0 if fp >= FREE_SHIP else SHIP_PRICE:.2f} EUR",
            "custom_label_0": p["range"],
            "custom_label_1": "<20" if fp < 20 else ("20-50" if fp < 50 else ("50-100" if fp < 100 else "100+")),
            "custom_label_2": p["labels"][0], "custom_label_3": p["labels"][1], "custom_label_4": p["labels"][2],
            "type_produit": p["type"],
        })

SIMPLE = ["id", "item_group_id", "title", "description", "link", "image_link", "additional_image_link", "availability", "availability_date",
          "price", "sale_price", "brand", "mpn", "identifier_exists", "condition", "google_product_category", "product_type",
          "color", "size", "size_system", "material", "age_group", "gender",
          "custom_label_0", "custom_label_1", "custom_label_2", "custom_label_3", "custom_label_4"]


def xml_item(r):
    out = ["    <item>"]
    for k in SIMPLE:
        if r[k]:
            tag = k if k in ("title", "description", "link") else f"g:{k}"
            out.append(f"      <{tag}>{xesc(r[k])}</{tag}>")
    c, _, _, sp = r["shipping"].split(":")
    out.append(f"      <g:shipping><g:country>{c}</g:country><g:service>Standard</g:service><g:price>{sp}</g:price></g:shipping>")
    out += [f"      <g:product_highlight>{xesc(h)}</g:product_highlight>" for h in r["product_highlight"]]
    out += [f"      <g:product_detail><g:section_name>{xesc(s)}</g:section_name><g:attribute_name>{xesc(a)}</g:attribute_name><g:attribute_value>{xesc(val)}</g:attribute_value></g:product_detail>" for s, a, val in r["product_detail"]]
    out.append("    </item>")
    return "\n".join(out)


with open(f"{OUT}/feeds/google-merchant.xml", "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">\n  <channel>\n'
            f'    <title>{BRAND} – flux produits</title>\n    <link>{BASE}/</link>\n    <description>Couches lavables hybrides Washie</description>\n'
            + "\n".join(xml_item(r) for r in rows) + "\n  </channel>\n</rss>\n")

cols = SIMPLE[:4] + ["short_description"] + SIMPLE[4:] + ["shipping", "product_highlight", "product_detail", "type_produit"]
with open(f"{OUT}/feeds/products.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(cols)
    for r in rows:
        w.writerow([",".join(r[c]) if c == "product_highlight" else (",".join(f"{s}:{a}:{val}".replace(",", " ") for s, a, val in r[c]) if c == "product_detail" else r[c]) for c in cols])

with open(f"{OUT}/feeds/products.json", "w", encoding="utf-8") as f:
    json.dump({"brand": BRAND, "currency": "EUR", "generated": TODAY, "count": len(rows),
               "products": [{**{k: r[k] for k in cols if k != "product_detail"},
                             "product_detail": [{"section": s, "attribute": a, "value": val} for s, a, val in r["product_detail"]]} for r in rows]},
              f, ensure_ascii=False, indent=2)

# ---------------------------------------------------------------- SEO / GEO
indexable = [n for n in pages if n not in ("panier.html", "mentions-legales.html", "confidentialite.html")]
pmap = {p["page"]: p for p in PRODUCTS}
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
for n in indexable:
    imgs = "".join(f"<image:image><image:loc>{abs_url(img)}</image:loc></image:image>" for img in sorted({v['image'] for v in pmap[n]['variants']})) if n in pmap else ""
    pr = "1.0" if n == "index.html" else "0.9" if n == "boutique.html" else "0.8" if n in pmap else "0.7"
    sm.append(f"  <url><loc>{abs_url(n)}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority>{imgs}</url>")
sm.append("</urlset>")
with open(f"{OUT}/sitemap.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(sm) + "\n")
with open(f"{OUT}/robots.txt", "w", encoding="utf-8") as f:
    f.write("User-agent: *\nAllow: /\nDisallow: /panier.html\n\n# Robots IA autorisés (GEO)\n"
            + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "Applebot-Extended", "Bingbot"])
            + f"Sitemap: {BASE}/sitemap.xml\n")

llms = [f"# {BRAND}", "",
        "> Washie conçoit des couches lavables hybrides pour bébé : une culotte douce, une poche étanche et un absorbant lavable ou jetable. "
        "Deux systèmes (Classic à poche intégrée, Switch à poche détachable), 5 tailles de 2 à 21 kg, absorbants jour, nuit, coton bio et jetables. "
        f"Livraison France métropolitaine {eur(SHIP_PRICE)}, offerte dès {eur(FREE_SHIP)}, retours gratuits 30 jours.", "",
        "## Guides",
        f"- [Quelle couche lavable choisir ?]({abs_url('guide-choisir-couche-lavable.html')}): systèmes, Classic vs Switch, quantités, budget",
        f"- [Guide des tailles]({abs_url('guide-des-tailles.html')}): XS 2–4 kg, S 4–8 kg, M 6–12 kg, L 9–17 kg, XL 14–21 kg ; absorbants T1/T2/T3",
        f"- [Laver ses couches lavables]({abs_url('guide-entretien-couches-lavables.html')}): routine, températures, lessive, fuites et odeurs",
        f"- [FAQ]({abs_url('faq.html')})", "", "## Produits"]
for p in PRODUCTS:
    pr = eur(p["final_price"]) + (f" (au lieu de {eur(p['price'])})" if p.get("sale_price") else "")
    llms.append(f"- [{p['name']}]({abs_url(p['page'])}): {p['type']}, {p['size']}, {pr}. {p['short']}")
llms += ["", "## Données", f"- [Flux produits XML]({abs_url('feeds/google-merchant.xml')})", f"- [Flux produits CSV]({abs_url('feeds/products.csv')})",
         f"- [Flux produits JSON]({abs_url('feeds/products.json')})", f"- [Plan du site]({abs_url('sitemap.xml')})"]
with open(f"{OUT}/llms.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(llms) + "\n")

print(f"OK : {len(pages)} pages, {len(rows)} variantes ({len(PRODUCTS)} produits) -> {OUT}/ (base {BASE}, GA4={'oui' if CFG.GA4_ID else 'non'})")
