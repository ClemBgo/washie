# -*- coding: utf-8 -*-
"""Illustrations produit (SVG -> PNG 1000x1000) pour le site et le flux.
Visuels vectoriels originaux : produit sur fond uni, sans texte promotionnel
(conforme aux exigences d'image principale Google Shopping)."""
import subprocess, os, html
from catalog import COLORS

BG = "#F6F1E9"


def tint(hexc, f=0.55):
    h = hexc.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r, g, b = [int(v + (255 - v) * f) for v in (r, g, b)]
    return f"#{r:02X}{g:02X}{b:02X}"


def darker(hexc, f=0.25):
    h = hexc.lstrip("#")
    r, g, b = [int(int(h[i:i + 2], 16) * (1 - f)) for i in (0, 2, 4)]
    return f"#{r:02X}{g:02X}{b:02X}"


DIAPER = ("M210 330 Q500 290 790 330 L815 430 Q720 470 655 590 Q610 705 500 715 "
          "Q390 705 345 590 Q280 470 185 430 Z")


def snaps(y=345, n=7, x0=290, x1=710, col="#FFFFFF", r=11):
    out = []
    for i in range(n):
        x = x0 + (x1 - x0) * i / (n - 1)
        out.append(f'<circle cx="{x:.0f}" cy="{y}" r="{r}" fill="{col}" opacity=".9"/>'
                   f'<circle cx="{x:.0f}" cy="{y}" r="{r*0.45:.0f}" fill="#000" opacity=".08"/>')
    return "".join(out)


def pattern_clouds(c):
    p = []
    for (x, y, s) in [(330, 420, 1), (520, 460, .8), (640, 400, .9), (450, 560, .7), (560, 610, .6), (400, 480, .5)]:
        p.append(f'<g transform="translate({x},{y}) scale({s})" fill="{c}" opacity=".55">'
                 '<circle cx="0" cy="0" r="18"/><circle cx="20" cy="-8" r="22"/><circle cx="42" cy="2" r="16"/>'
                 '<rect x="-2" y="0" width="46" height="16" rx="8"/></g>')
    return "".join(p)


def stars(c="#F3E3A6"):
    pts = [(320, 420), (450, 470), (600, 410), (530, 560), (400, 540), (660, 480), (480, 640)]
    out = []
    for x, y in pts:
        out.append(f'<path transform="translate({x},{y})" d="M0 -14 L4 -4 L14 0 L4 4 L0 14 L-4 4 L-14 0 L-4 -4Z" fill="{c}"/>')
    return "".join(out)


def diaper(c1, c2, scale=1.0, deco="clouds", cx=500, cy=500, trim="#FFFFFF"):
    deco_svg = {"clouds": pattern_clouds(tint(c1, .6)), "stars": stars(), "none": "",
                "waves": "".join(f'<path d="M260 {y} q30 -18 60 0 t60 0 t60 0 t60 0 t60 0 t60 0 t60 0 t60 0" '
                                 f'stroke="{tint(c1,.6)}" stroke-width="10" fill="none" opacity=".8"/>' for y in (420, 480, 540, 600)),
                "knit": "".join(f'<path d="M{x} 340 L{x} 700" stroke="{darker(c1,.08)}" stroke-width="6" '
                                f'stroke-dasharray="14 8" opacity=".7"/>' for x in range(250, 780, 34))}[deco]
    t = f'translate({cx - 500*scale},{cy - 500*scale}) scale({scale})'
    return f'''<g transform="{t}">
  <ellipse cx="500" cy="760" rx="260" ry="26" fill="#000" opacity=".07"/>
  <clipPath id="cl{abs(hash((c1,deco,scale,cx)))}"><path d="{DIAPER}"/></clipPath>
  <path d="{DIAPER}" fill="{c1}"/>
  <g clip-path="url(#cl{abs(hash((c1,deco,scale,cx)))})">{deco_svg}
    <path d="M185 430 Q280 470 345 590 Q390 705 500 715 Q610 705 655 590 Q720 470 815 430 L815 470 Q730 500 670 610 Q620 735 500 745 Q380 735 330 610 Q270 500 185 470Z" fill="{c2}"/>
  </g>
  <path d="M210 330 Q500 290 790 330 L795 352 Q500 315 205 352Z" fill="{trim}" opacity=".85"/>
  <path d="M300 520 Q330 600 380 650" stroke="{trim}" stroke-width="8" fill="none" stroke-linecap="round" opacity=".7" stroke-dasharray="3 12"/>
  <path d="M700 520 Q670 600 620 650" stroke="{trim}" stroke-width="8" fill="none" stroke-linecap="round" opacity=".7" stroke-dasharray="3 12"/>
  {snaps(col=trim if trim != "#FFFFFF" else "#FFFFFF")}
  <circle cx="230" cy="395" r="12" fill="#fff" opacity=".9"/><circle cx="770" cy="395" r="12" fill="#fff" opacity=".9"/>
</g>'''


def insert(c, w=560, h=200, layers=4, cx=500, cy=500, rot=-8):
    lines = "".join(f'<rect x="{-w/2+18+i*6}" y="{-h/2+18+i*6}" width="{w-36-i*12}" height="{h-36-i*12}" rx="{h/2-20}" '
                    f'fill="none" stroke="{darker(c,.12)}" stroke-width="3" stroke-dasharray="10 7" opacity=".6"/>' for i in range(1))
    stack = "".join(f'<rect x="{-w/2}" y="{-h/2 + (layers-i)*7}" width="{w}" height="{h}" rx="{h/2}" fill="{darker(c, .04*(layers-i))}"/>' for i in range(layers))
    return f'''<g transform="translate({cx},{cy}) rotate({rot})">
  <ellipse cx="0" cy="{h/2+40}" rx="{w/2}" ry="22" fill="#000" opacity=".07"/>{stack}{lines}</g>'''


def prefold(c, cx=500, cy=500):
    return f'''<g transform="translate({cx},{cy})">
  <ellipse cx="0" cy="290" rx="250" ry="24" fill="#000" opacity=".07"/>
  <rect x="-230" y="-260" width="460" height="520" rx="26" fill="{c}"/>
  <rect x="-230" y="-260" width="460" height="520" rx="26" fill="none" stroke="{darker(c,.12)}" stroke-width="4"/>
  <line x1="-78" y1="-250" x2="-78" y2="250" stroke="{darker(c,.15)}" stroke-width="4" stroke-dasharray="12 8"/>
  <line x1="78" y1="-250" x2="78" y2="250" stroke="{darker(c,.15)}" stroke-width="4" stroke-dasharray="12 8"/>
  <rect x="-78" y="-260" width="156" height="520" fill="{darker(c,.04)}"/>
  {''.join(f'<line x1="-215" y1="{y}" x2="215" y2="{y}" stroke="{darker(c,.06)}" stroke-width="2"/>' for y in range(-230,250,26))}
</g>'''


def roll(c, cx=500, cy=520):
    return f'''<g transform="translate({cx},{cy})">
  <ellipse cx="0" cy="230" rx="300" ry="24" fill="#000" opacity=".07"/>
  <path d="M-150 -160 L190 -160 Q260 -160 260 0 Q260 160 190 160 L-150 160Z" fill="{darker(c,.04)}"/>
  <path d="M-150 160 L-150 210 L330 210 L330 160Z" fill="{c}"/>
  <ellipse cx="-150" cy="0" rx="80" ry="160" fill="{c}"/>
  <ellipse cx="-150" cy="0" rx="72" ry="150" fill="none" stroke="{darker(c,.12)}" stroke-width="3"/>
  <ellipse cx="-150" cy="0" rx="26" ry="52" fill="{darker(c,.25)}"/>
  {''.join(f'<line x1="{x}" y1="165" x2="{x}" y2="205" stroke="{darker(c,.1)}" stroke-width="2"/>' for x in range(-140,330,12))}
</g>'''


def training(c1, c2, cx=500, cy=500):
    d = "M250 330 L750 330 L790 560 Q690 600 600 560 Q560 620 500 625 Q440 620 400 560 Q310 600 210 560Z"
    return f'''<g>
  <ellipse cx="500" cy="680" rx="280" ry="24" fill="#000" opacity=".07"/>
  <path d="{d}" fill="{c1}"/>
  <rect x="250" y="320" width="500" height="44" rx="14" fill="{c2}"/>
  {''.join(f'<line x1="{x}" y1="326" x2="{x}" y2="358" stroke="#fff" stroke-width="2" opacity=".4"/>' for x in range(262,742,14))}
  <path d="M440 470 Q500 510 560 470" stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round" opacity=".7"/>
  <circle cx="440" cy="430" r="9" fill="#fff" opacity=".8"/><circle cx="560" cy="430" r="9" fill="#fff" opacity=".8"/>
</g>'''


def bag(c1, c2):
    return f'''<g>
  <ellipse cx="500" cy="790" rx="250" ry="24" fill="#000" opacity=".07"/>
  <path d="M430 230 Q430 150 500 150 Q570 150 570 230" stroke="{c2}" stroke-width="26" fill="none"/>
  <rect x="290" y="230" width="420" height="540" rx="36" fill="{c1}"/>
  <rect x="290" y="230" width="420" height="70" rx="30" fill="{c2}"/>
  <line x1="320" y1="265" x2="680" y2="265" stroke="#fff" stroke-width="6" stroke-dasharray="6 6" opacity=".8"/>
  <rect x="660" y="252" width="20" height="40" rx="6" fill="#fff"/>
  <rect x="330" y="470" width="340" height="260" rx="24" fill="{darker(c1,.08)}"/>
  <line x1="350" y1="500" x2="650" y2="500" stroke="#fff" stroke-width="5" stroke-dasharray="5 5" opacity=".7"/>
</g>'''


def wipes(c):
    out = ['<ellipse cx="500" cy="700" rx="280" ry="24" fill="#000" opacity=".07"/>']
    for i in range(6):
        y = 640 - i * 34
        out.append(f'<rect x="{250 + (i%2)*12}" y="{y-110}" width="480" height="130" rx="16" fill="{darker(c, .02*(6-i))}" stroke="{darker(c,.12)}" stroke-width="2"/>')
    out.append(f'<path d="M260 390 l480 0" stroke="{darker(c,.15)}" stroke-width="3" stroke-dasharray="4 6"/>')
    return "".join(out)


def bottle(c1="#9DB59A", c2="#7E9A7B"):
    return f'''<g>
  <ellipse cx="500" cy="810" rx="200" ry="22" fill="#000" opacity=".07"/>
  <rect x="440" y="150" width="120" height="80" rx="14" fill="{c2}"/>
  <path d="M360 300 Q360 230 440 230 L560 230 Q640 230 640 300 L660 760 Q660 800 620 800 L380 800 Q340 800 340 760Z" fill="#FBF8F2" stroke="#E1D9CA" stroke-width="4"/>
  <rect x="370" y="420" width="260" height="270" rx="20" fill="{c1}"/>
  <circle cx="500" cy="520" r="52" fill="#fff" opacity=".35"/><circle cx="540" cy="500" r="40" fill="#fff" opacity=".35"/>
  <rect x="410" y="610" width="180" height="16" rx="8" fill="#fff" opacity=".7"/>
  <rect x="440" y="640" width="120" height="12" rx="6" fill="#fff" opacity=".5"/>
</g>'''


def pocket_shape(c, cx=500, cy=500, scale=1.0):
    d = "M-250 -120 Q0 -170 250 -120 L200 60 Q120 200 0 210 Q-120 200 -200 60 Z"
    return f'''<g transform="translate({cx},{cy}) scale({scale})">
  <ellipse cx="0" cy="260" rx="250" ry="22" fill="#000" opacity=".07"/>
  <path d="{d}" fill="{c}" stroke="{darker(c,.12)}" stroke-width="4"/>
  <path d="M-235 -110 Q0 -150 235 -110" stroke="{darker(c,.2)}" stroke-width="10" fill="none" stroke-linecap="round"/>
  <path d="M-200 40 Q-120 170 0 180 Q120 170 200 40" stroke="{darker(c,.2)}" stroke-width="8" fill="none" stroke-dasharray="4 10" stroke-linecap="round"/>
  <rect x="-275" y="-150" width="60" height="26" rx="8" fill="{darker(c,.35)}"/><rect x="215" y="-150" width="60" height="26" rx="8" fill="{darker(c,.35)}"/>
</g>'''


def inner_pocket(col="#FFFFFF"):
    return (f'<path d="M300 380 Q500 355 700 380 L660 470 Q610 600 500 640 Q390 600 340 470 Z" fill="{col}" opacity=".45"/>'
            f'<path d="M300 380 Q500 355 700 380" stroke="#fff" stroke-width="6" fill="none" opacity=".8"/>')


def disposable_stack():
    out = ['<ellipse cx="500" cy="720" rx="270" ry="22" fill="#000" opacity=".07"/>']
    for i in range(5):
        y = 640 - i * 40
        out.append(f'<rect x="{240 + (i%2)*10}" y="{y-90}" width="500" height="110" rx="55" fill="#FFFFFF" stroke="#E2DDD2" stroke-width="3"/>'
                   f'<rect x="{290 + (i%2)*10}" y="{y-62}" width="400" height="54" rx="27" fill="#F1EEE7"/>')
    return "".join(out)


def blob(c):
    return (f'<circle cx="500" cy="500" r="390" fill="{tint(c, .78)}"/>'
            f'<circle cx="780" cy="230" r="70" fill="{tint(c, .7)}"/>')


def product_svg(p, color):
    c1, c2 = COLORS.get(color, ("#9DB59A", "#7E9A7B"))
    s = p["shape"]
    body = ""
    if s == "diaper":
        body = diaper(c1, c2)
    elif s == "classic":
        body = diaper(c1, c2)[:-4] + inner_pocket() + "</g>"
    elif s == "switch":
        body = diaper(c1, c2, deco="none")[:-4] + inner_pocket("#FFFFFF") + '<rect x="285" y="372" width="40" height="22" rx="6" fill="#fff"/><rect x="675" y="372" width="40" height="22" rx="6" fill="#fff"/></g>'
    elif s == "pocket":
        body = pocket_shape("#FFFFFF", cy=430, scale=.8) + pocket_shape("#F4F1EA", cy=600, scale=.8)
    elif s == "insert_night":
        body = insert(c1, h=230, layers=5, cy=500, rot=-6) + stars()
    elif s == "disposable":
        body = disposable_stack()
    elif s == "kit_switch":
        body = (diaper(c1, c2, deco="none", scale=.62, cx=500, cy=400)[:-4] + "</g>" +
                pocket_shape("#FFFFFF", cx=330, cy=700, scale=.45) + pocket_shape("#F4F1EA", cx=670, cy=700, scale=.45))
    elif s == "diaper_small":
        body = diaper(c1, c2, scale=.82)
    elif s == "diaper_night":
        body = diaper(c1, c2, deco="stars")
    elif s == "cover":
        body = diaper(c1, c2, deco="none")
    elif s == "cover_wool":
        body = diaper(c1, c2, deco="knit", trim=darker(c1, .1))
    elif s == "swim":
        body = diaper(c1, c2, deco="waves")
    elif s == "prefold":
        body = prefold(c1)
    elif s == "insert":
        body = insert(c1, cx=500, cy=430) + insert(darker(c1, .03), cx=500, cy=590, rot=4)
    elif s == "insert_thin":
        body = insert(c1, h=150, layers=2, cy=430) + insert(c1, h=150, layers=2, cy=580, rot=5)
    elif s == "roll":
        body = roll(c1)
    elif s == "training":
        body = training(c1, c2)
    elif s == "bag":
        body = bag(c1, c2)
    elif s == "wipes":
        body = wipes(c1)
    elif s == "bottle":
        body = bottle()
    elif s == "kit_small":
        body = (diaper("#E0B24F", "#C79A39", scale=.55, cx=330, cy=380) +
                diaper("#6F8FAF", "#56789A", scale=.55, cx=680, cy=380) +
                diaper(c1, c2, scale=.62, cx=500, cy=560) +
                insert("#F3EEE3", w=300, h=100, layers=3, cx=500, cy=820, rot=0))
    elif s == "kit_big":
        body = "".join(diaper(col[0], col[1], scale=.36, cx=190 + (i % 4) * 207, cy=290 + (i // 4) * 200)
                       for i, col in enumerate([COLORS[k] for k in ["Sable", "Sauge", "Terracotta", "Ciel",
                                                                    "Moutarde", "Rose poudré", "Sable", "Sauge"]]))
        body += insert("#EFE6D2", w=360, h=110, layers=4, cx=500, cy=790, rot=0)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000" viewBox="0 0 1000 1000">'
            f'<rect width="1000" height="1000" fill="{BG}"/>{blob(c1)}{body}</svg>')


def detail_svg(p, color):
    """Visuel secondaire : fiche synthèse (image additionnelle)."""
    c1, c2 = COLORS.get(color, ("#9DB59A", "#7E9A7B"))
    lines = []
    y = 470
    for h in p.get("highlights", [])[:4]:
        lines.append(f'<circle cx="150" cy="{y-12}" r="14" fill="{c1}"/>'
                     f'<path d="M143 {y-12} l5 6 l10 -12" stroke="#fff" stroke-width="4" fill="none"/>'
                     f'<text x="185" y="{y}" font-family="Inter" font-size="38" fill="#2F3A33">{html.escape(h)}</text>')
        y += 78
    name = p["name"]
    # découpe du nom sur 2 lignes
    words, l1, l2 = name.split(), "", ""
    for w in words:
        if len(l1) + len(w) < 21 and not l2:
            l1 += (" " if l1 else "") + w
        else:
            l2 += (" " if l2 else "") + w
    small = product_svg(p, color).split('>', 1)[1].rsplit('</svg>', 1)[0]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="1000" viewBox="0 0 1000 1000">'
            f'<rect width="1000" height="1000" fill="#FFFDF9"/>'
            f'<g transform="translate(690,30) scale(.28)">{small}</g>'
            f'<text x="120" y="150" font-family="Inter" font-weight="600" font-size="30" fill="{darker(c1,.3)}" letter-spacing="3">{html.escape(p["type"].upper())}</text>'
            f'<text x="120" y="215" font-family="Inter Display" font-weight="700" font-size="50" fill="#2F3A33">{html.escape(l1)}</text>'
            f'<text x="120" y="275" font-family="Inter Display" font-weight="700" font-size="50" fill="#2F3A33">{html.escape(l2)}</text>'
            f'<text x="120" y="360" font-family="Inter" font-size="32" fill="#5B665E">{html.escape(p["size"])}</text>'
            f'{"".join(lines)}'
            f'<rect x="0" y="900" width="1000" height="100" fill="{tint(c1,.7)}"/>'
            f'<text x="120" y="962" font-family="Inter Display" font-weight="700" font-size="34" fill="#2F3A33">washie</text>'
            f'</svg>')


def render(svg, out_png, size=1000):
    tmp = out_png[:-4] + ".svg"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(svg)
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), "-f", "png", "-o", out_png, tmp], check=True)
    os.remove(tmp)
