#!/usr/bin/env python3
"""Generate the profile artwork: a holo trading card on a graffiti wall.

Philadelphia blue and red, white and silver foil. No team logos, marks or
wordmarks appear anywhere; every shape is original (TestBrand enforces it).

Three rules, all learned by breaking them:

1. NEVER put a CSS transform animation on an element that carries an SVG
   `transform` attribute. The CSS transform replaces the attribute rather than
   composing with it and the element snaps to the origin. Animate a child, or
   wrap the element in a positioned <g>.

2. The resting state must be the finished artwork. GitHub renders README
   images inside <img>; preview cards and thumbnailers can rasterise at t=0 or
   a few hundred ms in, without ever running the timeline to completion.
   Nothing essential may animate in from opacity 0, and no number may animate
   in from a wrong value.

3. Text is fitted, never hardcoded. fit() shrinks a string until it clears the
   space actually available, so copy changes cannot push type off an edge.

Every glyph is a vector outline: <img>-embedded SVG cannot load a webfont.
"""
import os

import card as C
import graffiti as G
import stats as ST
import motifs as MO
from text2path import load, text_path

# This file lives in the art folder and writes beside itself, so the
# generator works from a fresh clone rather than only from a dev layout.
OUT = os.path.dirname(os.path.abspath(__file__))

HELV = "/System/Library/Fonts/HelveticaNeue.ttc"
DIN = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"
black = load(HELV, 9)      # Helvetica Neue Condensed Black
din = load(DIN)            # DIN Condensed Bold

RED, BLUE, NAVY = "#c8102e", "#1d428a", "#0b2a5b"
DEEP, WHITE, BONE = "#061A38", "#FFFFFF", "#F2F5FA"
RED_TXT, BLUE_TXT = "#ff5a78", "#7FB0EE"   # tinted for small type on navy
THEME = {}


def set_theme(dark):
    THEME.clear()
    THEME.update(
        dark=dark,
        page=DEEP if dark else BONE,
        ink=WHITE if dark else NAVY,
        sub="#9DB8D6" if dark else "#54708C",
        dot=WHITE if dark else NAVY,
        dotop="0.13" if dark else "0.10",
    )


def P(f, t, s, tr=0.0):
    return text_path(f, t, s, tr)


def fit(f, t, s, max_w, tr=0.0, floor=7.0):
    while s > floor:
        d, w = P(f, t, s, tr)
        if w <= max_w:
            return d, w, s
        s -= 0.5
    d, w = P(f, t, s, tr)
    return d, w, s


def centered(f, t, s, cx, y, fill, max_w, tr=0.0, extra=""):
    d, w, _ = fit(f, t, s, max_w, tr)
    return f'<path d="{d}" fill="{fill}" transform="translate({cx-w/2:.1f} {y})" {extra}/>'


# =========================================================================
# HERO: a holo trading card on a graffiti wall
# =========================================================================
HERO_W, HERO_H = 1100, 960

REDUCED = """
      @media (prefers-reduced-motion: reduce) {
        * { animation: none !important }
      }"""


def card_facts():
    """Everything printed on the card. Playful, and every number is real."""
    return dict(
        hp=ST.MERGES,
        strip="Builder  \u00b7  Lead CAD Designer, FTC Team 23543  \u00b7  Fremont, CA",
        ability=dict(
            name="Parity Audit",
            text=(f"Check whether two code paths that should agree really do. "
                  f"{ST.MERGES} pull requests merged into {ST.REPOS} repositories "
                  f"across {ST.ORGS} organizations.")),
        moves=[
            dict(cost=["court", "code"], name="Fast Break Build",
                 damage=f"{ST.WINS}\u00d7",
                 text=(f"Ship a working app in one weekend. {ST.WINS} hackathon wins "
                       f"in 2026: SwarmMarket, ShadowBuyer, EcoLens and ShadowBuyer "
                       f"for Main Street.")),
            dict(cost=["build", "code", "code"], name="Digital Twin", damage="375",
                 text=("Rebuild the team robot in about 375 parts and test it in "
                       "MuJoCo. The redesign passed 59 of 59 ball positions in "
                       "simulation.")),
        ],
        wrr=[("WEAKNESS", "Flaky tests \u00d72"), ("RESISTANCE", "Cold starts -30"),
             ("RETREAT COST", "None")],
        flavor=("Captained the freshman team in 2025-26 and now plays varsity as "
                "the only sophomore. Reads issue trackers backwards for fun."),
        set="23543/2029",
    )


def hero():
    W, H = HERO_W, HERO_H
    uid = "H"
    t = THEME
    x0, y0 = (W - C.CW) / 2, 40
    facts = card_facts()
    label = (f"Shaurya Singh holo trading card. HP {ST.MERGES}. Ability Parity Audit: "
             f"{ST.MERGES} pull requests merged into {ST.REPOS} repositories across "
             f"{ST.ORGS} organizations. Fast Break Build: {ST.WINS} hackathon wins in "
             f"2026. Digital Twin: a 375-part robot tested in simulation.")
    body, card_css = C.card(uid, x0, y0, facts)

    s = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}">',
         f"<title>{label}</title>"]
    s.append(f"""<defs>
    {G.filters(uid)}
    {G.patterns(uid, t['dot'], t['dotop'])}
    {C.defs(uid)}
    <style><![CDATA[
      @keyframes drip{uid} {{ 0% {{ transform: scaleY(.88) }} 100% {{ transform: scaleY(1) }} }}
      @keyframes puff{uid} {{ 0%, 100% {{ opacity: .42 }} 50% {{ opacity: .78 }} }}
      .drip{uid} {{ animation: drip{uid} 3.4s ease-in-out infinite alternate;
                    transform-box: fill-box; transform-origin: top center }}
      .puff{uid} {{ animation: puff{uid} 5s ease-in-out infinite }}
      {card_css}
      {REDUCED}
    ]]></style>
  </defs>""")

    # Wall graffiti is inked in the opposite of the wall. White spray on a
    # light sheet is invisible spray.
    WI = WHITE if t["dark"] else NAVY
    s.append(f'<rect width="{W}" height="{H}" fill="{t["page"]}"/>')
    s.append(f'<rect width="{W}" height="{H}" fill="url(#dots{uid})"/>')
    s.append(f'<path d="M0 0 H300 L0 250 Z" fill="url(#slash{uid})" opacity=".5"/>')
    s.append(f'<path d="M{W} {H} H{W-300} L{W} {H-250} Z" fill="url(#slash{uid})" opacity=".5"/>')

    s.append(G.blob(150, 300, 140, 150, 11, WI, 0.055, uid=uid))
    s.append(G.blob(955, 640, 140, 160, 23, WI, 0.05, uid=uid))
    s.append(G.brush_stroke(30, 170, 250, 136, 46, 5, RED, 0.85, uid=uid))
    s.append(G.brush_stroke(1080, 800, 860, 830, 40, 8, BLUE, 0.85, uid=uid))
    s.append(G.brush_stroke(40, 640, 230, 672, 30, 12, BLUE, 0.6, uid=uid))
    s.append(G.brush_stroke(870, 190, 1080, 168, 26, 17, RED, 0.6, uid=uid))

    s.append(f'<g class="puff{uid}">{G.splatter(120, 400, 110, 31, RED, 18, 3, 14, .85, uid)}</g>')
    s.append(f'<g class="puff{uid}">{G.splatter(985, 340, 110, 44, BLUE, 20, 3, 15, .85, uid)}</g>')
    s.append(G.splatter(160, 840, 100, 57, WI, 16, 2, 10, .5, uid))
    s.append(G.splatter(950, 90, 100, 63, WI, 14, 2, 9, .45, uid))
    s.append(G.drips(48, 196, 200, 71, RED, 6, 30, 140, cls=f"drip{uid}"))
    s.append(G.drips(870, 850, 190, 83, BLUE, 5, 24, 70, cls=f"drip{uid}"))
    s.append(G.speckle(0, 0, W, H, 97, 230, WI, 0.34, 2.4))
    for bx, by, br in ((132, 560, 104), (968, 470, 96)):
        s.append(f'<g fill="none" stroke="{WI}" stroke-opacity=".13" stroke-width="7" '
                 f'transform="translate({bx} {by})">'
                 f'<circle r="{br}"/><line x1="{-br}" y1="0" x2="{br}" y2="0"/>'
                 f'<line x1="0" y1="{-br}" x2="0" y2="{br}"/>'
                 f'<path d="M{-br*0.66} {-br*0.75} C{-br*0.22} {-br*0.28} {-br*0.22} {br*0.28} {-br*0.66} {br*0.75}"/>'
                 f'<path d="M{br*0.66} {-br*0.75} C{br*0.22} {-br*0.28} {br*0.22} {br*0.28} {br*0.66} {br*0.75}"/></g>')
    s.append(G.splatter(60, 300, 70, 127, BLUE, 11, 2, 10, .6, uid))
    s.append(G.splatter(1050, 900, 80, 131, RED, 11, 2, 10, .6, uid))
    for sx, sy, sc, col in [
            (90, 96, 2.1, BLUE), (226, 70, 1.5, RED), (1030, 260, 2.0, RED),
            (1000, 900, 1.6, WI), (70, 880, 1.8, RED), (1060, 560, 1.3, BLUE),
            (180, 470, 1.2, WI)]:
        s.append(f'<g transform="translate({sx} {sy}) scale({sc})">'
                 f'<path d="{MO.STAR5}" fill="{col}" opacity=".85"/></g>')
    dv, wv, _ = fit(black, "ROOKIE", 46, 300, 5)
    s.append(f'<g transform="translate(46 {H/2 + wv/2}) rotate(-90)">'
             f'<path d="{dv}" fill="{WI}" opacity=".17"/></g>')
    dv2, wv2, _ = fit(black, "PHILADELPHIA", 40, 440, 4)
    s.append(f'<g transform="translate({W-36} {H/2 - wv2/2}) rotate(90)">'
             f'<path d="{dv2}" fill="{WI}" opacity=".15"/></g>')

    s.append(body)
    s.append(f'<rect width="{W}" height="{H}" filter="url(#grain{uid})" opacity=".7"/>')
    s.append("</svg>")
    return "\n".join(s)


# =========================================================================
# LEDGER
# =========================================================================
def ledger():
    W, H = 1200, 200
    uid = "L"
    t = THEME
    head = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-label="{ST.MERGES} merges landed, {ST.ORGS} organizations, {ST.REPOS} repositories, '
            f'{ST.WINS} hackathons won">',
            f"<title>{ST.MERGES} merges landed, {ST.ORGS} organizations, "
            f"{ST.REPOS} repositories, {ST.WINS} hackathons won</title>"]
    css, s = [], []
    ink = WHITE if t["dark"] else NAVY

    s.append(f'<rect width="{W}" height="{H}" fill="{NAVY if t["dark"] else WHITE}"/>')
    s.append(f'<rect width="{W}" height="{H}" fill="url(#dots{uid})"/>')
    s.append(G.brush_stroke(-20, 30, 420, 20, 26, 3, RED, .32, uid=uid))
    s.append(G.brush_stroke(1220, 176, 800, 184, 24, 6, BLUE, .32, uid=uid))
    s.append(G.speckle(0, 0, W, H, 19, 90, ink, 0.18, 2.0))
    s.append(f'<rect y="0" width="{W}" height="8" fill="{RED}"/>')
    s.append(f'<rect y="{H-8}" width="{W}" height="8" fill="{BLUE}"/>')
    s.append(G.drips(120, 8, 940, 27, RED, 7, 10, 34, cls=f"dr{uid}"))

    lab_r = RED_TXT if t["dark"] else RED
    lab_b = BLUE_TXT if t["dark"] else BLUE
    stats = [(str(ST.MERGES), "MERGES LANDED", lab_r),
             (str(ST.ORGS), "ORGANIZATIONS", lab_b),
             (str(ST.REPOS), "REPOSITORIES", lab_r),
             (str(ST.WINS), "HACKATHONS WON", lab_b)]
    slot = W / 4
    for i, (num, lab, col) in enumerate(stats):
        cx = slot * (i + 0.5)
        target = int(num)
        frames = sorted({int(target * p) for p in (0, .3, .58, .78, .9)} | {target})
        n = len(frames)
        lead, roll = 5.0, 80.0
        seg = roll / n
        for j, v in enumerate(frames):
            dv, wv = P(black, str(v), 78)
            a, b = lead + j * seg, lead + (j + 1) * seg
            cls = f"n{uid}{i}_{j}"
            if j == n - 1:
                kf = (f"@keyframes {cls}k{{0%,{lead-0.1:.1f}%{{opacity:1}}"
                      f"{lead:.1f}%,{lead+roll-seg:.1f}%{{opacity:0}}"
                      f"{lead+roll-seg+0.1:.1f}%,100%{{opacity:1}}}}")
                op = "1"
            else:
                # Ghosted: a frame caught mid-roll reads as a spinning counter,
                # never as a real figure. Only the truth is ever fully opaque.
                kf = (f"@keyframes {cls}k{{0%,{a-0.1:.1f}%{{opacity:0}}"
                      f"{a:.1f}%,{b:.1f}%{{opacity:.38}}"
                      f"{b+0.1:.1f}%,100%{{opacity:0}}}}")
                op = "0"
            css.append(f"{kf}.{cls}{{animation:{cls}k 1.5s linear forwards}}")
            s.append(f'<g class="{cls}" opacity="{op}" '
                     f'transform="translate({cx-wv/2:.1f} 104)"><path d="{dv}" fill="{ink}"/></g>')
        s.append(centered(din, lab, 22, cx, 152, col, slot - 34, 2.4))
        s.append(f'<rect x="{cx-36}" y="126" width="72" height="5" fill="{col}"/>')
        if i:
            s.append(f'<rect x="{slot*i-1}" y="46" width="2" height="112" '
                     f'fill="{ink}" opacity=".18"/>')

    s.append(f'<rect width="{W}" height="{H}" filter="url(#grain{uid})" opacity=".7"/>')
    s.append("</svg>")
    head.append(f"""<defs>
    {G.filters(uid)}
    {G.patterns(uid, t['dot'], t['dotop'])}
    <style><![CDATA[
      @keyframes dr{uid} {{ 0%{{transform:scaleY(.8)}} 100%{{transform:scaleY(1)}} }}
      .dr{uid} {{ animation: dr{uid} 3.6s ease-in-out infinite alternate;
                  transform-box: fill-box; transform-origin: top center }}
      {"".join(css)}
      {REDUCED}
    ]]></style>
  </defs>""")
    return "\n".join(head + s)


# =========================================================================
# SECTION HEADERS
# =========================================================================
def rule(name, num, title, accent):
    W, H = 1200, 104
    uid = "R" + name
    t = THEME
    ink = WHITE if t["dark"] else NAVY
    s = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="Section {num}: {title}">', f"<title>Section {num}: {title}</title>"]
    s.append(f"""<defs>
    {G.filters(uid)}
    {G.patterns(uid, t['dot'], t['dotop'])}
    <linearGradient id="sh{uid}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="50%" stop-color="#FFFFFF" stop-opacity="0.26"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
    <style><![CDATA[
      @keyframes sw{uid} {{ 0%{{transform:translateX(-320px)}} 100%{{transform:translateX(1460px)}} }}
      @keyframes dr{uid} {{ 0%{{transform:scaleY(.82)}} 100%{{transform:scaleY(1)}} }}
      .sw{uid} {{ animation: sw{uid} 7.5s cubic-bezier(.45,0,.55,1) infinite }}
      .dr{uid} {{ animation: dr{uid} 3.2s ease-in-out infinite alternate;
                  transform-box: fill-box; transform-origin: top center }}
      {REDUCED}
    ]]></style>
  </defs>""")
    s.append(f'<rect width="{W}" height="{H}" fill="{NAVY if t["dark"] else BONE}"/>')
    s.append(f'<rect width="{W}" height="{H}" fill="url(#dots{uid})"/>')
    s.append(G.speckle(0, 0, W, H, 61, 60, ink, 0.16, 1.8))
    s.append(f'<path d="M0 0 H176 L146 {H} H0 Z" fill="{accent}"/>')
    s.append(G.splatter(176, H/2, 54, 13, accent, 12, 2, 8, .8, uid))
    s.append(G.drips(16, H-4, 120, 21, accent, 4, 8, 22, cls=f"dr{uid}"))
    d, w = P(black, num, 52)
    s.append(f'<path d="{d}" fill="{WHITE}" transform="translate({72-w/2:.1f} {H/2+18:.1f})"/>')
    d, w, _ = fit(black, title.upper(), 46, 700, 1.4)
    s.append(f'<path d="{d}" fill="{ink}" transform="translate(228 {H/2+17:.1f})"/>')
    s.append(f'<rect x="{228+w+28}" y="{H/2-2}" width="{max(40, W-330-w)}" height="4" '
             f'fill="{accent}" opacity=".55"/>')
    s.append(f'<g class="sw{uid}"><rect x="-320" y="0" width="200" height="{H}" '
             f'fill="url(#sh{uid})" transform="skewX(-20)"/></g>')
    s.append(f'<rect width="{W}" height="{H}" filter="url(#grain{uid})" opacity=".7"/>')
    s.append("</svg>")
    return "\n".join(s)


SECTIONS = [
    ("career", "01", "Career Highlights", RED),
    ("builds", "02", "Featured Builds", BLUE),
    ("merges", "03", "The Merge Docket", RED),
    ("lab", "04", "In the Lab", BLUE),
    ("court", "05", "Off the Court", RED),
    ("stack", "06", "The Stack", BLUE),
    ("gamelog", "07", "Game Log", RED),
    ("reach", "08", "Reach Me", BLUE),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    total = 0
    for dark in (False, True):
        set_theme(dark)
        suf = "-dark" if dark else ""
        files = {f"hero{suf}.svg": hero(), f"ledger{suf}.svg": ledger()}
        for nm, num, title, accent in SECTIONS:
            files[f"rule-{nm}{suf}.svg"] = rule(nm, num, title, accent)
        for fn, body in files.items():
            with open(os.path.join(OUT, fn), "w") as f:
                f.write(body)
            total += len(body)
            print(f"{fn:24} {len(body)/1024:6.1f} KB")
    print(f"{'total':24} {total/1024:6.1f} KB")


if __name__ == "__main__":
    main()
