#!/usr/bin/env python3
"""Generate the profile artwork — 76ers broadcast graphics.

Visual language: hard diagonal colour blocks, ben-day halftone, diagonal
hatching, a thirteen-star arc, red/white/blue stripe bars, and heavy
condensed type. Drawn from the team's palette and the 1776 star motif; the
"76" lockup here is original artwork, not a trace of the team's logo.

Two rules the previous version learned the hard way, both load-bearing:

1. NEVER put a CSS transform animation on an element that carries an SVG
   `transform` attribute. The CSS transform replaces the attribute instead of
   composing with it and the element snaps to the origin. Animate a child, or
   wrap the element in a positioned <g>.

2. The resting state must be the finished artwork. GitHub renders README
   images inside <img>; link-preview cards and thumbnailers may rasterise at
   t=0 without ever advancing the timeline. Nothing essential may animate in
   from opacity 0, and no number may animate in from a wrong value. SMIL
   counters therefore carry their FINAL value as the element attribute, so a
   frozen render shows the truth and a live render plays the count-up.

Every glyph is emitted as vector outlines, because <img>-embedded SVG cannot
load a webfont.
"""
import math
import os
from text2path import load, text_path

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profile", "art")

HELV = "/System/Library/Fonts/HelveticaNeue.ttc"
DIN = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"

black = load(HELV, 9)      # Helvetica Neue Condensed Black — the wordmark
cbold = load(HELV, 4)      # Helvetica Neue Condensed Bold
din = load(DIN)            # DIN Condensed Bold — labels, broadcast furniture

# ---- palette -------------------------------------------------------------
BLUE = "#006BB6"
RED = "#ED174C"
NAVY = "#002B5C"
DEEP = "#00203F"
WHITE = "#FFFFFF"
BONE = "#EEF2F7"

THEME = {}


def set_theme(dark: bool):
    """Light = white sheet with navy type. Dark = navy field with white type."""
    THEME.clear()
    THEME.update(
        dark=dark,
        field=DEEP if dark else BONE,
        field2=NAVY if dark else WHITE,
        ink=WHITE if dark else NAVY,
        sub="#9FB6D0" if dark else "#5A7189",
        dots=WHITE if dark else NAVY,
        dotop="0.10" if dark else "0.07",
    )


def P(font, text, size, tracking=0.0):
    return text_path(font, text, size, tracking)


def fit(font, text, size, max_w, tracking=0.0, floor=8.0):
    """Shrink until the string fits max_w. Nothing may run past its frame."""
    while size > floor:
        d, w = P(font, text, size, tracking)
        if w <= max_w:
            return d, w, size
        size -= 1.0
    d, w = P(font, text, size, tracking)
    return d, w, size


# ---- shared defs ---------------------------------------------------------
def defs(uid, extra=""):
    t = THEME
    return f"""<defs>
    <pattern id="ht{uid}" width="9" height="9" patternUnits="userSpaceOnUse">
      <circle cx="2.2" cy="2.2" r="1.7" fill="{t['dots']}" opacity="{t['dotop']}"/>
    </pattern>
    <pattern id="htb{uid}" width="14" height="14" patternUnits="userSpaceOnUse">
      <circle cx="3.4" cy="3.4" r="3.0" fill="{WHITE}" opacity="0.16"/>
    </pattern>
    <pattern id="hatch{uid}" width="13" height="13" patternUnits="userSpaceOnUse"
             patternTransform="rotate(-38)">
      <rect width="5" height="13" fill="{WHITE}" opacity="0.22"/>
    </pattern>
    <filter id="grain{uid}" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="4" seed="11" result="n"/>
      <feColorMatrix in="n" type="saturate" values="0"/>
      <feComponentTransfer><feFuncA type="linear" slope="0.07"/></feComponentTransfer>
    </filter>
    <filter id="rough{uid}" x="-8%" y="-8%" width="116%" height="116%">
      <feTurbulence type="fractalNoise" baseFrequency="0.028" numOctaves="4" seed="5" result="t"/>
      <feDisplacementMap in="SourceGraphic" in2="t" scale="6"
                         xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <linearGradient id="sheen{uid}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{WHITE}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{WHITE}" stop-opacity="0.30"/>
      <stop offset="100%" stop-color="{WHITE}" stop-opacity="0"/>
    </linearGradient>{extra}
  </defs>"""


STAR = ("M0,-10 L2.7,-3.4 L9.6,-3.1 L4.1,1.4 L6.0,8.1 "
        "L0,4.1 L-6.0,8.1 L-4.1,1.4 L-9.6,-3.1 L-2.7,-3.4 Z")


def stripe_bars(x, y, h, w=7, gap=5, on_dark=None):
    """The red/white/blue bar stack off the team's flag.

    The middle bar is white on a dark field and navy on a light one —
    a white bar on the light sheet is an invisible bar.
    """
    if on_dark is None:
        on_dark = THEME.get("dark", True)
    mid = WHITE if on_dark else NAVY
    return "".join(
        f'<rect x="{x + i*(w+gap)}" y="{y}" width="{w}" height="{h}" fill="{c}"/>'
        for i, c in enumerate((RED, mid, BLUE)))


def mark76(uid, cx, cy, r, animate=True):
    """Original 76 roundel: star arc over a red 7 and a blue 6."""
    s = [f'<g transform="translate({cx} {cy})">']
    spin = f' class="spin{uid}"' if animate else ""
    s.append(f'  <g{spin}>')
    s.append(f'    <circle r="{r}" fill="{WHITE}"/>')
    s.append(f'    <circle r="{r-7}" fill="none" stroke="{BLUE}" stroke-width="9"/>')
    s.append(f'    <circle r="{r-21}" fill="none" stroke="{RED}" stroke-width="3" opacity=".85"/>')
    s.append("  </g>")
    # thirteen stars, arcing across the top like the 1776 ring
    for i in range(13):
        a = math.radians(-172 + i * (164 / 12))
        sx, sy = (r - 36) * math.cos(a), (r - 36) * math.sin(a)
        s.append(f'  <g transform="translate({sx:.1f} {sy:.1f}) scale({r/230:.3f})">'
                 f'<path class="tw{uid} k{uid}{i}" d="{STAR}" fill="{BLUE}"/></g>')
    # The numerals, sized to sit inside the inner ring rather than punch
    # through it: fit the pair to the ring's chord, not to the outer radius.
    inner = r - 30
    size = r * 1.15
    for _ in range(40):
        d7, w7 = P(black, "7", size)
        d6, w6 = P(black, "6", size)
        if w7 + w6 + r * 0.04 <= inner * 1.45:
            break
        size -= r * 0.03
    total = w7 + w6 + r * 0.04
    x0 = -total / 2
    base = size * 0.36
    s.append(f'  <path d="{d7}" fill="{RED}" transform="translate({x0:.1f} {base:.1f})"/>')
    s.append(f'  <path d="{d6}" fill="{BLUE}" '
             f'transform="translate({x0 + w7 + r*0.04:.1f} {base:.1f})"/>')
    s.append("</g>")
    return "\n".join(s)


# =========================================================================
# HERO
# =========================================================================
def hero():
    W, H = 1200, 440
    t = THEME
    uid = "H"
    s = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="Shaurya Singh — builder of agents, fixer of other people\'s code">']

    star_css = "".join(
        f".k{uid}{i}{{animation:pop{uid} 3.2s ease-in-out infinite {0.9+i*0.09:.2f}s}}"
        for i in range(13))
    s.append(defs(uid, f"""
    <style><![CDATA[
      /* Motion only. Nothing here reveals essential content from nothing. */
      @keyframes pop{uid} {{ 0%,100% {{opacity:.45}} 50% {{opacity:1}} }}
      @keyframes sweep{uid} {{ 0% {{transform:translateX(-460px)}} 100% {{transform:translateX(1500px)}} }}
      @keyframes drift{uid} {{ 0% {{transform:translate(0,0)}} 100% {{transform:translate(9px,9px)}} }}
      @keyframes breathe{uid} {{ 0%,100% {{transform:scale(1)}} 50% {{transform:scale(1.022)}} }}
      @keyframes bar{uid} {{ 0% {{transform:scaleX(.55)}} 100% {{transform:scaleX(1)}} }}
      .sw{uid} {{ animation: sweep{uid} 6.5s cubic-bezier(.5,0,.5,1) infinite }}
      .dr{uid} {{ animation: drift{uid} 7s linear infinite alternate }}
      .spin{uid} {{ animation: breathe{uid} 4.5s ease-in-out infinite;
                    transform-box: fill-box; transform-origin: center }}
      .tw{uid} {{ transform-box: fill-box; transform-origin: center }}
      .b1{uid} {{ animation: bar{uid} 1.4s cubic-bezier(.16,1,.3,1) both; transform-origin: left center }}
      {star_css}
    ]]></style>"""))

    # --- field ------------------------------------------------------------
    s.append(f'<rect width="{W}" height="{H}" fill="{t["field"]}"/>')
    # blue block cut on a hard diagonal, the broadcast wedge
    s.append(f'<path d="M690 0 H{W} V{H} H560 Z" fill="{BLUE}"/>')
    s.append(f'<path d="M690 0 H{W} V{H} H560 Z" fill="url(#htb{uid})"/>')
    # red keyline riding the diagonal
    s.append(f'<path d="M672 0 L542 {H} L566 {H} L696 0 Z" fill="{RED}"/>')
    s.append(f'<path d="M655 0 L525 {H} L533 {H} L663 0 Z" fill="{RED}" opacity=".55"/>')
    # halftone across the light side + a hatched corner
    s.append(f'<g class="dr{uid}"><rect width="700" height="{H}" fill="url(#ht{uid})"/></g>')
    s.append(f'<path d="M{W-230} 0 H{W} V150 Z" fill="url(#hatch{uid})"/>')

    # --- splatter: a few rough marks so it reads printed, not vector -------
    # Kept clear of the type column; ink spots behind words read as dirt.
    s.append(f'<g filter="url(#rough{uid})" opacity=".45">')
    for cx_, cy_, rr, col in ((738, 372, 16, WHITE), (795, 404, 10, WHITE),
                              (1042, 58, 13, WHITE), (1112, 104, 8, WHITE),
                              (632, 42, 9, RED)):
        s.append(f'  <circle cx="{cx_}" cy="{cy_}" r="{rr}" fill="{col}" opacity=".45"/>')
    s.append("</g>")

    # --- stripe bars, off the team flag ------------------------------------
    s.append(stripe_bars(46, 52, H - 104))

    # --- the 76 roundel ----------------------------------------------------
    s.append(mark76(uid, 966, 214, 132))

    # --- wordmark. Every string is fitted to the space actually available at
    # its own baseline: the blue wedge leans left as it descends, so a width
    # that clears it at the top runs underneath it lower down.
    left = 108

    def room(y, pad=22):
        """Usable width at baseline y, stopping short of the red keyline."""
        return (655 - 130 * y / H) - left - pad

    d1, w1, sz1 = fit(black, "SHAURYA", 104, room(196), tracking=2.0)
    d2, w2, sz2 = fit(black, "SINGH", 104, room(284), tracking=2.0)
    sz = min(sz1, sz2)
    d1, w1 = P(black, "SHAURYA", sz, 2.0)
    d2, w2 = P(black, "SINGH", sz, 2.0)
    s.append(f'<path d="{d1}" fill="{t["ink"]}" transform="translate({left} 196)"/>')
    s.append(f'<path d="{d2}" fill="{t["ink"]}" transform="translate({left} 284)"/>')

    # rule under the wordmark
    s.append(f'<g class="b1{uid}" style="transform-origin:{left}px 306px">')
    s.append(f'  <rect x="{left}" y="300" width="150" height="9" fill="{RED}"/>')
    s.append(f'  <rect x="{left+158}" y="300" width="92" height="9" fill="{BLUE}"/>')
    s.append("</g>")

    # --- supporting type ---------------------------------------------------
    dt, wt, _ = fit(din, "BUILDER OF AGENTS  ·  FIXER OF OTHER PEOPLE'S CODE",
                    26, room(348), tracking=1.4)
    s.append(f'<path d="{dt}" fill="{t["ink"]}" opacity=".92" transform="translate({left} 348)"/>')
    dk, wk, _ = fit(din, "100 MERGES  ·  21 ORGANIZATIONS  ·  CLASS OF 2029",
                    21, room(382), tracking=1.1)
    s.append(f'<path d="{dk}" fill="{t["sub"]}" transform="translate({left} 382)"/>')

    dn, wn, _ = fit(din, "PHILADELPHIA 76ERS  ·  FREMONT, CALIFORNIA", 19, room(92), tracking=1.4)
    s.append(f'<path d="{dn}" fill="{t["sub"]}" transform="translate({left} 92)"/>')

    # --- light sweep across the whole card ---------------------------------
    s.append(f'<rect class="sw{uid}" x="-460" y="0" width="300" height="{H}" '
             f'fill="url(#sheen{uid})" transform="skewX(-18)"/>')
    s.append(f'<rect width="{W}" height="{H}" filter="url(#grain{uid})" opacity=".8"/>')
    s.append("</svg>")
    return "\n".join(s)


# =========================================================================
# LEDGER — broadcast lower-third with real count-up
# =========================================================================
def ledger():
    W, H = 1200, 190
    t = THEME
    uid = "L"
    head = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-label="100 merges landed, 21 organizations, 44 repositories, 2 hackathons won">']
    css_frames = []
    s = []

    s.append(f'<rect width="{W}" height="{H}" fill="{NAVY if t["dark"] else WHITE}"/>')
    s.append(f'<rect width="{W}" height="{H}" fill="url(#ht{uid})"/>')
    s.append(f'<rect y="0" width="{W}" height="7" fill="{RED}"/>')
    s.append(f'<rect y="{H-7}" width="{W}" height="7" fill="{BLUE}"/>')

    ink = WHITE if t["dark"] else NAVY
    stats = [("100", "MERGES LANDED", RED), ("21", "ORGANIZATIONS", BLUE),
             ("44", "REPOSITORIES", RED), ("2", "HACKATHONS WON", BLUE)]
    slot = W / 4
    for i, (num, lab, col) in enumerate(stats):
        cx = slot * (i + 0.5)
        target = int(num)
        # Roll-up frames, driven by CSS rather than SMIL. Both the 0% and the
        # 100% keyframe of every frame hold the RESTING state — final number
        # visible, intermediates hidden — so a renderer stuck at t=0 and one
        # that runs to completion both show the true figure. The count-up only
        # exists in between.
        frames = sorted({int(target * p) for p in (0, .28, .55, .74, .87, .95)} | {target})
        n = len(frames)
        lead, roll = 6.0, 88.0          # percent of the 1.4s cycle
        seg = roll / n
        for j, v in enumerate(frames):
            dv, wv = P(black, str(v), 74)
            a, b = lead + j * seg, lead + (j + 1) * seg
            cls = f"n{uid}{i}_{j}"
            if j == n - 1:
                kf = (f"@keyframes {cls}k{{0%,{lead-0.1:.1f}%{{opacity:1}}"
                      f"{lead:.1f}%,{lead+roll-seg:.1f}%{{opacity:0}}"
                      f"{lead+roll-seg+0.1:.1f}%,100%{{opacity:1}}}}")
                op = "1"
            else:
                # Intermediates are ghosted, never solid: if anything snaps a
                # frame mid-roll it reads as a spinning counter rather than as
                # a real figure. Only the true number is ever fully opaque.
                kf = (f"@keyframes {cls}k{{0%,{a-0.1:.1f}%{{opacity:0}}"
                      f"{a:.1f}%,{b:.1f}%{{opacity:.42}}"
                      f"{b+0.1:.1f}%,100%{{opacity:0}}}}")
                op = "0"
            css_frames.append(f"{kf}.{cls}{{animation:{cls}k 1.4s linear forwards}}")
            s.append(f'<g class="{cls}" opacity="{op}" '
                     f'transform="translate({cx - wv/2:.1f} 96)">'
                     f'<path d="{dv}" fill="{ink}"/></g>')
        dl, wl, _ = fit(din, lab, 21, slot - 40, tracking=2.4)
        s.append(f'<path d="{dl}" fill="{col}" transform="translate({cx-wl/2:.1f} 146)"/>')
        s.append(f'<g class="u{uid}" style="transform-origin:{cx}px 116px">'
                 f'<rect x="{cx-34}" y="112" width="68" height="5" fill="{col}"/></g>')
        if i < 3:
            s.append(f'<rect x="{slot*(i+1)-1}" y="42" width="2" height="100" '
                     f'fill="{ink}" opacity=".16"/>')

    s.append(f'<rect class="sw{uid}" x="-400" y="0" width="240" height="{H}" '
             f'fill="url(#sheen{uid})" transform="skewX(-18)"/>')
    s.append(f'<rect width="{W}" height="{H}" filter="url(#grain{uid})" opacity=".7"/>')
    s.append("</svg>")
    head.append(defs(uid, f"""
    <style><![CDATA[
      @keyframes sweep{uid} {{ 0% {{transform:translateX(-400px)}} 100% {{transform:translateX(1500px)}} }}
      @keyframes bar{uid} {{ from {{transform:scaleX(.3)}} to {{transform:scaleX(1)}} }}
      .sw{uid} {{ animation: sweep{uid} 7s cubic-bezier(.5,0,.5,1) infinite }}
      .u{uid} {{ animation: bar{uid} 1.1s cubic-bezier(.16,1,.3,1) both }}
      {"".join(css_frames)}
    ]]></style>"""))
    return "\n".join(head + s)


# =========================================================================
# SECTION HEADERS
# =========================================================================
def rule(name, num, title, accent):
    W, H = 1200, 92
    t = THEME
    uid = "R" + name
    s = [f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{title}">']
    s.append(defs(uid, f"""
    <style><![CDATA[
      @keyframes sweep{uid} {{ 0% {{transform:translateX(-300px)}} 100% {{transform:translateX(1450px)}} }}
      @keyframes grow{uid} {{ from {{transform:scaleX(.82)}} to {{transform:scaleX(1)}} }}
      .sw{uid} {{ animation: sweep{uid} 8s cubic-bezier(.5,0,.5,1) infinite }}
      .g{uid} {{ animation: grow{uid} 1.2s cubic-bezier(.16,1,.3,1) both; transform-origin: 0 0 }}
    ]]></style>"""))

    s.append(f'<rect width="{W}" height="{H}" fill="{NAVY if t["dark"] else BONE}"/>')
    s.append(f'<rect width="{W}" height="{H}" fill="url(#ht{uid})"/>')
    # numeral block with a hard diagonal trailing edge
    s.append(f'<path d="M0 0 H150 L124 {H} H0 Z" fill="{accent}"/>')
    s.append(f'<path d="M150 0 H172 L146 {H} H124 Z" fill="{accent}" opacity=".28"/>')
    dnum, wnum = P(black, num, 46)
    s.append(f'<path d="{dnum}" fill="{WHITE}" transform="translate({64-wnum/2:.1f} 63)"/>')

    ink = WHITE if t["dark"] else NAVY
    dt, wt, _ = fit(black, title.upper(), 42, 760, tracking=1.4)
    s.append(f'<path d="{dt}" fill="{ink}" transform="translate(208 62)"/>')
    # trailing rule + stripe bars on the right
    s.append(f'<g class="g{uid}" style="transform-origin:{208+wt+26}px 46px">'
             f'<rect x="{208+wt+26}" y="43" width="{max(40, W-260-wt-90)}" height="3" '
             f'fill="{accent}" opacity=".6"/></g>')
    s.append(stripe_bars(W - 62, 22, H - 44))
    s.append(f'<rect class="sw{uid}" x="-300" y="0" width="180" height="{H}" '
             f'fill="url(#sheen{uid})" transform="skewX(-18)"/>')
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
