#!/usr/bin/env python3
"""Generate the profile artwork — a 76ers graffiti rookie card.

The 76ers marks are trademarks of the Philadelphia 76ers / NBA; this is a fan
rendition on a personal page.

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

import graffiti as G
import sixers_mark as SM
from text2path import load, text_path

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profile", "art")

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
# HERO — the rookie card
# =========================================================================
def hero():
    W, H = 1200, 680
    uid = "H"
    t = THEME
    CX = W / 2
    CW, CH = 452, 588                      # card size
    CXL, CYT = CX - CW / 2, 48             # card top-left
    s = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="Shaurya Singh rookie card — builder of agents, '
         f'100 merges landed">']

    stars_css = ""
    s.append(f"""<defs>
    {G.filters(uid)}
    {G.patterns(uid, t['dot'], t['dotop'])}
    <clipPath id="card{uid}">
      <rect x="{CXL}" y="{CYT}" width="{CW}" height="{CH}" rx="18"/>
    </clipPath>
    <linearGradient id="foil{uid}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#8FC7F5"/><stop offset="18%" stop-color="#FFFFFF"/>
      <stop offset="36%" stop-color="{RED}"/><stop offset="54%" stop-color="#FFFFFF"/>
      <stop offset="72%" stop-color="{BLUE}"/><stop offset="88%" stop-color="#CFE6FA"/>
      <stop offset="100%" stop-color="#8FC7F5"/>
      <animate attributeName="x1" values="0%;-100%;0%" dur="9s" repeatCount="indefinite"/>
      <animate attributeName="x2" values="100%;0%;100%" dur="9s" repeatCount="indefinite"/>
    </linearGradient>
    <linearGradient id="holo{uid}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="38%" stop-color="#BFE3FF" stop-opacity="0.30"/>
      <stop offset="50%" stop-color="#FFFFFF" stop-opacity="0.62"/>
      <stop offset="62%" stop-color="#FFC7D8" stop-opacity="0.30"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="plate{uid}" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#17407f"/><stop offset="100%" stop-color="#08214a"/>
    </linearGradient>
    <style><![CDATA[
      /* Motion only — every element is already visible at rest. */
      @keyframes bob{uid} {{ 0%,100%{{transform:scale(1)}} 50%{{transform:scale(1.028)}} }}
      .badge{uid} {{ animation: bob{uid} 5.5s ease-in-out infinite;
                     transform-box: fill-box; transform-origin: center }}
      @keyframes holo{uid} {{ 0%{{transform:translateX(-620px)}} 100%{{transform:translateX(1360px)}} }}
      @keyframes tilt{uid} {{ 0%,100%{{transform:rotate(-.5deg) scale(1)}}
                              50%{{transform:rotate(.5deg) scale(1.008)}} }}
      @keyframes drip{uid} {{ 0%{{transform:scaleY(.88)}} 100%{{transform:scaleY(1)}} }}
      @keyframes puff{uid} {{ 0%,100%{{opacity:.42}} 50%{{opacity:.78}} }}
      .holo{uid} {{ animation: holo{uid} 4.6s cubic-bezier(.45,0,.55,1) infinite }}
      .card{uid} {{ animation: tilt{uid} 9s ease-in-out infinite;
                    transform-box: fill-box; transform-origin: center }}
      .drip{uid} {{ animation: drip{uid} 3.4s ease-in-out infinite alternate;
                    transform-box: fill-box; transform-origin: top center }}
      .puff{uid} {{ animation: puff{uid} 5s ease-in-out infinite }}
      {stars_css}
    ]]></style>
  </defs>""")

    # Wall graffiti has to be inked in the opposite of the wall. White spray
    # on a light sheet is invisible spray.
    WI = WHITE if t["dark"] else NAVY
    # ---------------- background: the wall ----------------
    s.append(f'<rect width="{W}" height="{H}" fill="{t["page"]}"/>')
    s.append(f'<rect width="{W}" height="{H}" fill="url(#dots{uid})"/>')
    s.append(f'<path d="M0 0 H300 L0 250 Z" fill="url(#slash{uid})" opacity=".5"/>')
    s.append(f'<path d="M{W} {H} H{W-300} L{W} {H-250} Z" fill="url(#slash{uid})" opacity=".5"/>')

    # rough colour masses either side of the card
    s.append(G.blob(190, 250, 150, 132, 11, WI, 0.055, uid=uid))
    s.append(G.blob(1010, 430, 158, 138, 23, WI, 0.05, uid=uid))
    s.append(G.brush_stroke(60, 150, 330, 118, 46, 5, RED, 0.85, uid=uid))
    s.append(G.brush_stroke(1150, 560, 880, 592, 40, 8, BLUE, 0.85, uid=uid))
    s.append(G.brush_stroke(70, 470, 300, 505, 30, 12, BLUE, 0.6, uid=uid))
    s.append(G.brush_stroke(900, 150, 1140, 128, 26, 17, RED, 0.6, uid=uid))

    s.append(f'<g class="puff{uid}">{G.splatter(150, 330, 130, 31, RED, 20, 3, 15, .85, uid)}</g>')
    s.append(f'<g class="puff{uid}">{G.splatter(1040, 260, 140, 44, BLUE, 22, 3, 16, .85, uid)}</g>')
    s.append(G.splatter(240, 600, 120, 57, WI, 16, 2, 10, .5, uid))
    s.append(G.splatter(960, 90, 110, 63, WI, 14, 2, 9, .45, uid))

    s.append(G.drips(78, 176, 250, 71, RED, 6, 30, 130, cls=f"drip{uid}"))
    s.append(G.drips(900, 610, 240, 83, BLUE, 5, 24, 66, cls=f"drip{uid}"))
    s.append(G.speckle(0, 0, W, H, 97, 210, WI, 0.34, 2.4))
    # ghosted basketballs behind the wall clutter
    for bx, by, br in ((176, 452, 120), (1024, 196, 104)):
        s.append(f'<g fill="none" stroke="{WI}" stroke-opacity=".13" stroke-width="7" '
                 f'transform="translate({bx} {by})">'
                 f'<circle r="{br}"/><line x1="{-br}" y1="0" x2="{br}" y2="0"/>'
                 f'<line x1="0" y1="{-br}" x2="0" y2="{br}"/>'
                 f'<path d="M{-br*0.66} {-br*0.75} C{-br*0.22} {-br*0.28} {-br*0.22} {br*0.28} {-br*0.66} {br*0.75}"/>'
                 f'<path d="M{br*0.66} {-br*0.75} C{br*0.22} {-br*0.28} {br*0.22} {br*0.28} {br*0.66} {br*0.75}"/></g>')
    s.append(G.splatter(320, 120, 90, 111, WI, 12, 2, 8, .35, uid))
    s.append(G.splatter(880, 520, 100, 119, WI, 13, 2, 9, .35, uid))
    s.append(G.splatter(60, 250, 80, 127, BLUE, 11, 2, 10, .6, uid))
    s.append(G.splatter(1150, 620, 90, 131, RED, 11, 2, 10, .6, uid))
    s.append(G.drips(240, 500, 90, 137, WI, 3, 14, 40, cls=f"drip{uid}"))

    # loose stars on the wall
    for sx, sy, sc, col in [
            (110, 92, 2.1, BLUE), (268, 62, 1.5, RED), (1128, 214, 2.0, RED),
            (1062, 596, 1.6, WI), (86, 604, 1.8, RED), (1150, 420, 1.3, BLUE),
            (196, 424, 1.2, WI)]:
        s.append(f'<g transform="translate({sx} {sy}) scale({sc})">'
                 f'<path d="{SM.STAR5}" fill="{col}" opacity=".85"/></g>')

    # vertical spray tags down the margins
    dv, wv, _ = fit(black, "ROOKIE", 46, 300, 5)
    s.append(f'<g transform="translate(52 {H/2 + wv/2}) rotate(-90)">'
             f'<path d="{dv}" fill="{WI}" opacity=".17"/></g>')
    dv2, wv2, _ = fit(black, "PHILADELPHIA", 40, 420, 4)
    s.append(f'<g transform="translate({W-40} {H/2 - wv2/2}) rotate(90)">'
             f'<path d="{dv2}" fill="{WI}" opacity=".15"/></g>')

    # ---------------- the card ----------------
    s.append(f'<g class="card{uid}">')
    s.append(f'<rect x="{CXL-9}" y="{CYT-9}" width="{CW+18}" height="{CH+18}" rx="24" '
             f'fill="#00050C" opacity=".55"/>')
    s.append(f'<rect x="{CXL-7}" y="{CYT-7}" width="{CW+14}" height="{CH+14}" rx="22" '
             f'fill="url(#foil{uid})"/>')
    s.append(f'<rect x="{CXL-1}" y="{CYT-1}" width="{CW+2}" height="{CH+2}" rx="19" '
             f'fill="{NAVY}"/>')

    s.append(f'<g clip-path="url(#card{uid})">')
    s.append(f'<rect x="{CXL}" y="{CYT}" width="{CW}" height="{CH}" fill="url(#plate{uid})"/>')
    s.append(f'<rect x="{CXL}" y="{CYT}" width="{CW}" height="{CH}" fill="url(#dotsL{uid})"/>')
    s.append(G.blob(CX, CYT + 208, 168, 138, 77, WHITE, 0.10, uid=uid))
    s.append(G.brush_stroke(CXL + 20, CYT + 372, CXL + CW - 24, CYT + 392, 26, 33, BLUE, .5, uid=uid))
    s.append(G.splatter(CXL + 60, CYT + 330, 90, 41, RED, 13, 2, 9, .45, uid))
    s.append(G.splatter(CXL + CW - 66, CYT + 150, 84, 49, BLUE, 12, 2, 9, .45, uid))
    s.append(G.speckle(CXL, CYT, CW, CH, 53, 70, WHITE, 0.22, 1.9))
    s.append(f'<path d="M{CXL} {CYT} H{CXL+160} L{CXL} {CYT+150} Z" '
             f'fill="url(#slash{uid})" opacity=".55"/>')

    # Top strip. Everything sits left of the corner flash, which would
    # otherwise swallow a right-aligned date.
    pad = 26
    d, w, _ = fit(din, "ROOKIE CARD", 22, 200, 2.6)
    s.append(f'<path d="{d}" fill="{WHITE}" opacity=".92" '
             f'transform="translate({CXL+pad} {CYT+42})"/>')
    d2, w2, _ = fit(din, "2026", 22, 80, 2.6)
    s.append(f'<path d="{d2}" fill="{RED_TXT}" transform="translate({CXL+pad+w+16} {CYT+42})"/>')
    s.append(f'<rect x="{CXL+pad}" y="{CYT+54}" width="{CW-2*pad}" height="2" '
             f'fill="{WHITE}" opacity=".28"/>')

    # The real 76ers badge, centred in the panel between the hairline and the
    # name plate. Sized to the smaller of the panel's height and width.
    py = CYT + 346                     # top rule of the name plate
    panel_top, panel_bot = CYT + 70, py - 26
    dia = min(panel_bot - panel_top, CW - 2 * pad - 30)
    s.append(f'<g class="badge{uid}">'
             f'{SM.badge(CX, (panel_top + panel_bot) / 2, dia)}</g>')
    s.append(f'<rect x="{CXL+pad}" y="{py}" width="{CW-2*pad}" height="3" fill="{RED}"/>')
    s.append(centered(black, "SHAURYA SINGH", 52, CX, py + 60, WHITE, CW - 2*pad - 10, 0))
    s.append(centered(din, "BUILDER OF AGENTS  ·  FIXER OF OTHER PEOPLE'S CODE",
                      21, CX, py + 86, "#AFC6E6", CW - 2*pad - 8, 1.0))
    s.append(f'<rect x="{CXL+pad}" y="{py+102}" width="{CW-2*pad}" height="3" fill="{BLUE}"/>')

    sy = py + 172
    cells = [("100", "MERGES"), ("21", "ORGS"), ("44", "REPOS"), ("2", "WINS")]
    cw = (CW - 2 * pad) / len(cells)
    for i, (n, lab) in enumerate(cells):
        ccx = CXL + pad + cw * (i + 0.5)
        s.append(centered(black, n, 34, ccx, sy, WHITE, cw - 8))
        s.append(centered(din, lab, 16, ccx, sy + 21, RED_TXT if i % 2 == 0 else BLUE_TXT,
                          cw - 6, 1.6))
        if i:
            s.append(f'<rect x="{CXL+pad+cw*i:.1f}" y="{sy-28}" width="1.5" height="48" '
                     f'fill="{WHITE}" opacity=".2"/>')

    s.append(f'<path d="M{CXL+CW} {CYT} L{CXL+CW} {CYT+96} L{CXL+CW-96} {CYT} Z" fill="{RED}"/>')
    d, w = P(black, "RC", 30)
    s.append(f'<g transform="translate({CXL+CW-34} {CYT+30}) rotate(45)">'
             f'<path d="{d}" fill="{WHITE}" transform="translate({-w/2:.1f} 10)"/></g>')

    s.append(f'<g class="holo{uid}"><rect x="{CXL-620}" y="{CYT-60}" width="230" '
             f'height="{CH+120}" fill="url(#holo{uid})" transform="skewX(-20)"/></g>')
    s.append("</g>")   # clip
    s.append("</g>")   # card

    s.append(f'<rect width="{W}" height="{H}" filter="url(#grain{uid})" opacity=".85"/>')
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
            f'aria-label="100 merges landed, 21 organizations, 44 repositories, '
            f'2 hackathons won">']
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
    stats = [("100", "MERGES LANDED", lab_r), ("21", "ORGANIZATIONS", lab_b),
             ("44", "REPOSITORIES", lab_r), ("2", "HACKATHONS WON", lab_b)]
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
         f'aria-label="Section {num} — {title}">']
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
    ("stack", "04", "The Stack", BLUE),
    ("court", "05", "Off the Court", RED),
    ("reach", "06", "Reach Me", BLUE),
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
