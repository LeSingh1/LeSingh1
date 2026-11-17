#!/usr/bin/env python3
"""The holo trading card at the centre of the hero.

Laid out like a collectible battle card: stage pill and name bar, HP and a
type symbol, a foil art window, an info strip, one ability and two moves with
damage numbers, weakness / resistance / retreat, flavour text, then the
illustrator line, set number and rarity star.

Everything on it is true. HP is the merge count, the moves carry real numbers,
and the set number is the FTC team number. Every shape is original: the art
window shows a ball dropping through a net under the thirteen-star arc, which
is the 1776 colonies device and belongs to nobody.

Placement transforms live on static elements only. Anything that moves is a
wrapper <g> with no transform attribute of its own (see art/README.md, rule 2).
"""
import math

import graffiti as G
import motifs as MO
from text2path import load, text_path

HELV = "/System/Library/Fonts/HelveticaNeue.ttc"
GILL = "/System/Library/Fonts/Supplemental/GillSans.ttc"
DIN = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"
BLACK = load(HELV, 9)          # Helvetica Neue Condensed Black
GILL_R = load(GILL, 0)         # Gill Sans
GILL_B = load(GILL, 1)         # Gill Sans Bold
GILL_SB = load(GILL, 4)        # Gill Sans SemiBold
GILL_I = load(GILL, 2)         # Gill Sans Italic
DINC = load(DIN)

RED, BLUE, NAVY = "#c8102e", "#1d428a", "#0b2a5b"
WHITE = "#FFFFFF"
PALE = "#AFC6E6"               # small type on navy
SOFT = "#E6EEF9"               # body type on navy
ROSE = "#ff5a78"               # red tuned for small type on navy

# Card geometry, in hero coordinates.
CW, CH = 620, 880
FRAME = 18                     # silver border thickness
PAD = 16                       # face padding


def n(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def fit(font, s, size, max_w, tracking=0.0, floor=8.0):
    while size > floor:
        d, w = text_path(font, s, size, tracking)
        if w <= max_w:
            return d, w, size
        size -= 0.5
    d, w = text_path(font, s, size, tracking)
    return d, w, size


def type_at(font, s, size, x, y, fill, anchor="start", tracking=0.0,
            max_w=None, extra=""):
    if max_w:
        d, w, _ = fit(font, s, size, max_w, tracking)
    else:
        d, w = text_path(font, s, size, tracking)
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    return (f'<path d="{d}" fill="{fill}" transform="translate({n(x)} {n(y)})"'
            f'{extra}/>'), w


WS = 2.2                       # extra word space for Gill Sans body copy


def body(font, s, size, x, y, fill):
    d, w = text_path(font, s, size, 0.0, word_spacing=WS)
    return f'<path d="{d}" fill="{fill}" transform="translate({n(x)} {n(y)})"/>'


def wrap(font, s, size, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if cur and text_path(font, trial, size, 0.0, word_spacing=WS)[1] > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    return lines + ([cur] if cur else [])


# ------------------------------------------------------------------ symbols
def ball_lines(cx, cy, r, stroke, w):
    """Basketball seams: two verticals curving out, plus the equator."""
    k = r * 0.62
    return (f'<g fill="none" stroke="{stroke}" stroke-width="{w}" '
            f'stroke-linecap="round">'
            f'<path d="M{n(cx - r)} {n(cy)}H{n(cx + r)}"/>'
            f'<path d="M{n(cx)} {n(cy - r)}V{n(cy + r)}"/>'
            f'<path d="M{n(cx - k)} {n(cy - r * .79)}C{n(cx - r * .2)} {n(cy - r * .3)} '
            f'{n(cx - r * .2)} {n(cy + r * .3)} {n(cx - k)} {n(cy + r * .79)}"/>'
            f'<path d="M{n(cx + k)} {n(cy - r * .79)}C{n(cx + r * .2)} {n(cy - r * .3)} '
            f'{n(cx + r * .2)} {n(cy + r * .3)} {n(cx + k)} {n(cy + r * .79)}"/></g>')


def energy(kind, cx, cy, r=13):
    """Original energy symbols: court (ball), code (</>), build (gear)."""
    ring = (f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r + 1.6)}" fill="#0a1f45"/>')
    if kind == "court":
        return (ring + f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="#e6334d"/>'
                + ball_lines(cx, cy, r * 0.86, "#3a0712", 1.5))
    if kind == "code":
        s = r * 0.42
        return (ring + f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="#3d72c8"/>'
                f'<path d="M{n(cx - s * .55)} {n(cy - s)}L{n(cx - s * 1.45)} {n(cy)}'
                f'L{n(cx - s * .55)} {n(cy + s)}M{n(cx + s * .55)} {n(cy - s)}'
                f'L{n(cx + s * 1.45)} {n(cy)}L{n(cx + s * .55)} {n(cy + s)}'
                f'M{n(cx + s * .28)} {n(cy - s * 1.15)}L{n(cx - s * .28)} {n(cy + s * 1.15)}" '
                f'fill="none" stroke="{WHITE}" stroke-width="2" stroke-linecap="round" '
                f'stroke-linejoin="round"/>')
    # build: a gear
    teeth = []
    for i in range(8):
        a = math.radians(i * 45)
        tx, ty = cx + math.cos(a) * r * 0.62, cy + math.sin(a) * r * 0.62
        teeth.append(f'<rect x="{n(-2.4)}" y="{n(-2.6)}" width="4.8" height="5.2" '
                     f'transform="translate({n(tx)} {n(ty)}) rotate({i * 45})"/>')
    return (ring + f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="#dfe6f0"/>'
            f'<g fill="{NAVY}">{"".join(teeth)}'
            f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r * .56)}"/></g>'
            f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r * .22)}" fill="#dfe6f0"/>')


def star_path(cx, cy, s, fill):
    return (f'<g transform="translate({n(cx)} {n(cy)}) scale({s})">'
            f'<path d="{MO.STAR5}" fill="{fill}"/></g>')


# ------------------------------------------------------------------ defs
def defs(uid):
    return f"""
    <linearGradient id="silver{uid}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/><stop offset="16%" stop-color="#c3ccd8"/>
      <stop offset="34%" stop-color="#f6f8fb"/><stop offset="52%" stop-color="#94a1b4"/>
      <stop offset="70%" stop-color="#eef2f7"/><stop offset="86%" stop-color="#aab5c4"/>
      <stop offset="100%" stop-color="#f3f6fa"/>
    </linearGradient>
    <linearGradient id="bevelHi{uid}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity=".95"/>
      <stop offset="50%" stop-color="#ffffff" stop-opacity=".15"/>
      <stop offset="100%" stop-color="#2b3a52" stop-opacity=".55"/>
    </linearGradient>
    <linearGradient id="bevelLo{uid}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1a2638" stop-opacity=".7"/>
      <stop offset="50%" stop-color="#1a2638" stop-opacity=".1"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity=".85"/>
    </linearGradient>
    <linearGradient id="face{uid}" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#2352a3"/><stop offset="42%" stop-color="#17407f"/>
      <stop offset="100%" stop-color="#0a2552"/>
    </linearGradient>
    <radialGradient id="glow{uid}" cx="50%" cy="48%" r="60%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity=".34"/>
      <stop offset="55%" stop-color="#ffffff" stop-opacity=".06"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="ballG{uid}" cx="36%" cy="30%" r="78%">
      <stop offset="0%" stop-color="#ff5a6e"/><stop offset="45%" stop-color="{RED}"/>
      <stop offset="100%" stop-color="#7a0a1e"/>
    </radialGradient>
    <linearGradient id="foil{uid}" x1="0" y1="0" x2="130" y2="130"
                    gradientUnits="userSpaceOnUse" spreadMethod="repeat">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="22%" stop-color="#8fc7f5" stop-opacity=".55"/>
      <stop offset="38%" stop-color="#ffffff" stop-opacity=".75"/>
      <stop offset="54%" stop-color="#ff8fa3" stop-opacity=".5"/>
      <stop offset="72%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="sweep{uid}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="40%" stop-color="#cfe6ff" stop-opacity=".22"/>
      <stop offset="50%" stop-color="#ffffff" stop-opacity=".55"/>
      <stop offset="60%" stop-color="#ffd0da" stop-opacity=".22"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="strip{uid}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#dfe6ef"/><stop offset="50%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#c7d0dc"/>
    </linearGradient>
    <filter id="shadow{uid}" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="14"/>
    </filter>"""


CSS = """
      @keyframes holo{u} {{ 0% {{ transform: translateX(-760px) }} 100% {{ transform: translateX(1500px) }} }}
      @keyframes foil{u} {{ 0% {{ transform: translate(0px, 0px) }} 100% {{ transform: translate(-260px, -260px) }} }}
      @keyframes tw{u} {{ 0%, 100% {{ opacity: .6 }} 50% {{ opacity: 1 }} }}
      .holo{u} {{ animation: holo{u} 5.2s cubic-bezier(.45,0,.55,1) infinite }}
      .foil{u} {{ animation: foil{u} 7s linear infinite }}
      {stars}"""


# ------------------------------------------------------------------ card
def card(uid, x0, y0, facts):
    """Return (markup, css) for the card with its top-left at (x0, y0)."""
    u = uid
    out = []
    fx0, fy0 = x0 + FRAME, y0 + FRAME
    fx1, fy1 = x0 + CW - FRAME, y0 + CH - FRAME
    cx0, cx1 = fx0 + PAD, fx1 - PAD              # content columns
    cmid = (x0 + x0 + CW) / 2

    out.append(f'<clipPath id="cardclip{u}"><rect x="{x0}" y="{y0}" width="{CW}" '
               f'height="{CH}" rx="26"/></clipPath>')

    # shadow on the wall, then the silver frame with a bevel
    out.append(f'<rect x="{x0 + 10}" y="{y0 + 22}" width="{CW}" height="{CH}" rx="26" '
               f'fill="#00050c" opacity=".55" filter="url(#shadow{u})"/>')
    out.append(f'<rect x="{x0}" y="{y0}" width="{CW}" height="{CH}" rx="26" '
               f'fill="url(#silver{u})"/>')
    out.append(f'<rect x="{x0 + 1.5}" y="{y0 + 1.5}" width="{CW - 3}" height="{CH - 3}" '
               f'rx="25" fill="none" stroke="url(#bevelHi{u})" stroke-width="3"/>')
    out.append(f'<rect x="{fx0 - 4}" y="{fy0 - 4}" width="{fx1 - fx0 + 8}" '
               f'height="{fy1 - fy0 + 8}" rx="15" fill="none" '
               f'stroke="url(#bevelLo{u})" stroke-width="3"/>')

    # the face: blue, a red pinstripe, halftone and spray
    out.append(f'<rect x="{fx0 - 1}" y="{fy0 - 1}" width="{fx1 - fx0 + 2}" '
               f'height="{fy1 - fy0 + 2}" rx="13" fill="{RED}"/>')
    out.append(f'<clipPath id="face{u}c"><rect x="{fx0 + 2}" y="{fy0 + 2}" '
               f'width="{fx1 - fx0 - 4}" height="{fy1 - fy0 - 4}" rx="11"/></clipPath>')
    out.append(f'<g clip-path="url(#face{u}c)">')
    out.append(f'<rect x="{fx0}" y="{fy0}" width="{fx1 - fx0}" height="{fy1 - fy0}" '
               f'fill="url(#face{u})"/>')
    out.append(f'<rect x="{fx0}" y="{fy0}" width="{fx1 - fx0}" height="{fy1 - fy0}" '
               f'fill="url(#dotsL{u})" opacity=".55"/>')
    out.append(G.splatter(fx0 + 40, fy0 + 470, 90, 41, RED, 12, 2, 8, .28, u))
    out.append(G.splatter(fx1 - 40, fy0 + 640, 90, 49, WHITE, 12, 2, 7, .12, u))
    out.append(G.speckle(fx0, fy0, fx1 - fx0, fy1 - fy0, 53, 80, WHITE, 0.16, 1.7))
    out.append(f'<path d="M{fx1} {fy0} H{fx1 - 150} L{fx1} {fy0 + 140} Z" '
               f'fill="url(#slash{u})" opacity=".35"/>')
    out.append("</g>")

    # ---------------- header: stage, name, HP, type
    pill_y = fy0 + 12
    out.append(f'<rect x="{cx0}" y="{pill_y}" width="98" height="24" rx="5" fill="{RED}"/>')
    t, _ = type_at(DINC, "STAGE 2", 18, cx0 + 49, pill_y + 19, WHITE, "middle", 1.6)
    out.append(t)
    t, _ = type_at(GILL_I, "Evolves from Freshman", 16, cx0 + 110, pill_y + 18, PALE)
    out.append(t)

    name_y = fy0 + 74
    t, wname = type_at(BLACK, "Shaurya Singh", 46, cx0, name_y, WHITE)
    out.append(t)
    # HP block, right-aligned against the type symbol
    sym_r = 19
    sym_cx = cx1 - sym_r
    out.append(f'<circle cx="{sym_cx}" cy="{name_y - 15}" r="{sym_r + 2.5}" fill="#0a1f45"/>')
    out.append(f'<circle cx="{sym_cx}" cy="{name_y - 15}" r="{sym_r}" fill="url(#ballG{u})"/>')
    out.append(ball_lines(sym_cx, name_y - 15, sym_r * .78, "#0a1f45", 2))
    t, whp = type_at(BLACK, str(facts["hp"]), 44, sym_cx - sym_r - 12, name_y, WHITE, "end")
    out.append(t)
    t, _ = type_at(DINC, "HP", 20, sym_cx - sym_r - 18 - whp, name_y - 1, ROSE, "end", 1)
    out.append(t)
    t, _ = type_at(DINC, "OPEN SOURCE  ·  ROBOTICS  ·  HACKATHONS  ·  CLASS OF 2029",
                   14.5, cx0, name_y + 21, PALE, tracking=1.3, max_w=cx1 - cx0)
    out.append(t)

    # ---------------- art window
    ax0, ay0, ax1, ay1 = cx0, fy0 + 110, cx1, fy0 + 360
    out.append(f'<rect x="{ax0 - 7}" y="{ay0 - 7}" width="{ax1 - ax0 + 14}" '
               f'height="{ay1 - ay0 + 14}" rx="6" fill="url(#silver{u})"/>')
    out.append(f'<rect x="{ax0 - 6}" y="{ay0 - 6}" width="{ax1 - ax0 + 12}" '
               f'height="{ay1 - ay0 + 12}" rx="5" fill="none" '
               f'stroke="url(#bevelHi{u})" stroke-width="2"/>')
    out.append(f'<clipPath id="art{u}"><rect x="{ax0}" y="{ay0}" width="{ax1 - ax0}" '
               f'height="{ay1 - ay0}" rx="2"/></clipPath>')
    out.append(f'<g clip-path="url(#art{u})">')
    out.append(art(u, ax0, ay0, ax1, ay1))
    out.append("</g>")
    out.append(f'<rect x="{ax0}" y="{ay0}" width="{ax1 - ax0}" height="{ay1 - ay0}" '
               f'rx="2" fill="none" stroke="#0a1f45" stroke-width="1.5"/>')

    # ---------------- info strip and 1st edition stamp
    sy0, sy1 = ay1 + 13, ay1 + 37
    out.append(f'<path d="M{cx0 + 40} {sy0} H{cx1} L{cx1 - 10} {sy1} H{cx0 + 30} Z" '
               f'fill="url(#strip{u})"/>')
    t, _ = type_at(GILL_SB, facts["strip"], 14.5, (cx0 + 30 + cx1) / 2, sy1 - 7, NAVY,
                   "middle", 0.4, max_w=cx1 - cx0 - 70)
    out.append(t)
    stx, sty = cx0 + 14, (sy0 + sy1) / 2
    out.append(f'<circle cx="{stx}" cy="{sty}" r="17" fill="#0a1f45" stroke="{WHITE}" '
               f'stroke-width="1.6"/>')
    t, _ = type_at(BLACK, "1", 17, stx, sty + 2.5, WHITE, "middle")
    out.append(t)
    t, _ = type_at(DINC, "EDITION", 6.4, stx, sty + 10.5, WHITE, "middle", 0.6)
    out.append(t)

    # ---------------- ability and moves
    y = sy1 + 26
    body_w = cx1 - cx0
    ab = facts["ability"]
    out.append(f'<rect x="{cx0}" y="{y}" width="92" height="24" rx="5" fill="{RED}"/>')
    t, _ = type_at(DINC, "ABILITY", 18, cx0 + 46, y + 19, WHITE, "middle", 1.6)
    out.append(t)
    t, _ = type_at(GILL_B, ab["name"], 27, cx0 + 106, y + 21, ROSE)
    out.append(t)
    y += 46
    for ln in wrap(GILL_R, ab["text"], 17.5, body_w):
        out.append(body(GILL_R, ln, 17.5, cx0, y, SOFT))
        y += 21.5
    for mv in facts["moves"]:
        y += 2
        out.append(f'<rect x="{cx0}" y="{n(y - 12)}" width="{body_w}" height="1.4" '
                   f'fill="{WHITE}" opacity=".28"/>')
        y += 22
        ix = cx0 + 14
        for kind in mv["cost"]:
            out.append(energy(kind, ix, y - 8))
            ix += 31
        t, _ = type_at(GILL_B, mv["name"], 27, ix + 6, y + 1, WHITE)
        out.append(t)
        t, _ = type_at(BLACK, mv["damage"], 38, cx1, y + 4, WHITE, "end")
        out.append(t)
        y += 30
        for ln in wrap(GILL_R, mv["text"], 17.5, body_w):
            out.append(body(GILL_R, ln, 17.5, cx0, y, SOFT))
            y += 21.5

    # ---------------- weakness / resistance / retreat
    y += 2
    out.append(f'<rect x="{cx0}" y="{n(y - 12)}" width="{body_w}" height="2" '
               f'fill="{WHITE}" opacity=".45"/>')
    col = body_w / 3
    for i, (lab, val) in enumerate(facts["wrr"]):
        x = cx0 + col * i
        t, _ = type_at(DINC, lab, 14, x, y + 6, PALE, tracking=1.2)
        out.append(t)
        t, _ = type_at(GILL_SB, val, 16.5, x, y + 27, WHITE, max_w=col - 12)
        out.append(t)

    # ---------------- flavour text
    by0 = y + 36
    lines = wrap(GILL_I, facts["flavor"], 15.5, body_w - 28)
    bh = 16 + 19.5 * len(lines)
    out.append(f'<rect x="{cx0}" y="{n(by0)}" width="{body_w}" height="{n(bh)}" rx="4" '
               f'fill="#061a38" fill-opacity=".45" stroke="{PALE}" stroke-opacity=".55" '
               f'stroke-width="1.2"/>')
    ty = by0 + 21
    for ln in lines:
        out.append(body(GILL_I, ln, 15.5, cx0 + 14, ty, SOFT))
        ty += 19.5

    # ---------------- footer: illustrator, set number, rarity
    fy = fy1 - 12
    if ty > fy - 22:
        raise ValueError(f"card copy overflows the face by {ty - fy + 22:.0f}px")
    t, _ = type_at(DINC, "ILLUS. ART/BUILD_ART.PY", 13.5, cx0, fy, PALE, tracking=1.2)
    out.append(t)
    t, wset = type_at(DINC, facts["set"], 15, cx1 - 18, fy, WHITE, "end", 1.2)
    out.append(t)
    out.append(star_path(cx1 - 7, fy - 5.5, 0.72, WHITE))
    t, _ = type_at(DINC, "© 2026 LESINGH1", 13.5, cmid, fy, PALE, "middle", 1.2)
    out.append(t)

    # ---------------- the holo sweep across the whole card
    out.append(f'<g clip-path="url(#cardclip{u})"><g class="holo{u}">'
               f'<rect x="{x0 - 300}" y="{y0 - 80}" width="260" height="{CH + 160}" '
               f'fill="url(#sweep{u})" transform="skewX(-18)"/></g></g>')

    stars_css = "".join(
        f".st{u}{i} {{ animation: tw{u} 3.2s ease-in-out infinite {i * 0.12:.2f}s }}"
        for i in range(13))
    return "\n".join(out), CSS.format(u=u, stars=stars_css)


def art(u, x0, y0, x1, y1):
    """The illustration: a ball dropping through a net under the star arc."""
    w, h = x1 - x0, y1 - y0
    cx = (x0 + x1) / 2
    out = []
    # sunburst from behind the hoop
    ox, oy = cx + 40, y0 + h * 0.62
    rays = []
    for i in range(28):
        a0 = 2 * math.pi * i / 28
        a1 = a0 + 2 * math.pi / 56
        R = 900
        rays.append(f"M{n(ox)} {n(oy)}L{n(ox + R * math.cos(a0))} {n(oy + R * math.sin(a0))}"
                    f"L{n(ox + R * math.cos(a1))} {n(oy + R * math.sin(a1))}Z")
    out.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="#17407f"/>')
    out.append(f'<path d="{"".join(rays)}" fill="#2a5bb0" opacity=".55"/>')
    out.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="url(#glow{u})"/>')
    out.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="url(#dots{u})" '
               f'opacity=".6"/>')
    # paint on the wall behind the play
    out.append(G.brush_stroke(x0 - 10, y1 - 34, x0 + w * .52, y1 - 58, 44, 71, RED, .85, uid=u))
    out.append(G.brush_stroke(x1 + 10, y0 + 70, x0 + w * .62, y0 + 92, 30, 73, "#0b2a5b", .7,
                              uid=u))
    out.append(G.splatter(x0 + 70, y0 + 96, 70, 77, WHITE, 12, 2, 7, .5, u))
    out.append(G.splatter(x1 - 60, y1 - 60, 70, 79, RED, 12, 2, 8, .7, u))

    # thirteen stars arcing over the play
    out.append(MO.star_arc(cx, y0 + 108, w * 0.36, 70, size=1.15, fill=WHITE,
                           cls=f"st{u}"))

    # the shot: a dashed arc from lower left into the rim
    bx, by, br = cx + 52, y0 + 122, 48          # ball
    rim_cx, rim_cy, rim_rx, rim_ry = cx + 64, y0 + 172, 70, 13
    sx, sy = x0 + 36, y1 - 40
    out.append(f'<path d="M{n(sx)} {n(sy)}Q{n(cx - 110)} {n(y0 + 30)} {n(bx - br * .9)} '
               f'{n(by - br * .45)}" fill="none" stroke="{WHITE}" stroke-width="4" '
               f'stroke-dasharray="2 13" stroke-linecap="round" opacity=".75"/>')
    # rim, back half
    out.append(f'<path d="M{n(rim_cx - rim_rx)} {n(rim_cy)}A{rim_rx} {rim_ry} 0 0 1 '
               f'{n(rim_cx + rim_rx)} {n(rim_cy)}" fill="none" stroke="#7a0a1e" '
               f'stroke-width="7"/>')
    # backboard in side view, with its bracket
    bbx, bbt, bbb = rim_cx + rim_rx + 24, rim_cy - 66, rim_cy + 30
    out.append(f'<rect x="{n(rim_cx + rim_rx - 4)}" y="{n(rim_cy - 4)}" width="30" '
               f'height="8" fill="#c9d3e0"/>')
    out.append(f'<rect x="{n(bbx)}" y="{n(bbt)}" width="16" height="{n(bbb - bbt)}" rx="2" '
               f'fill="#f4f7fb" stroke="#0a1f45" stroke-width="2"/>')
    out.append(f'<rect x="{n(bbx + 4)}" y="{n(bbt + 6)}" width="8" '
               f'height="{n(bbb - bbt - 12)}" fill="{RED}"/>')
    out.append(f'<path d="M{n(bbx + 16)} {n(rim_cy - 20)}L{n(x1 + 2)} {n(rim_cy - 44)}'
               f'M{n(bbx + 16)} {n(rim_cy + 14)}L{n(x1 + 2)} {n(rim_cy + 34)}" '
               f'stroke="#c9d3e0" stroke-width="6"/>')
    # ball
    out.append(f'<circle cx="{n(bx + 6)}" cy="{n(by + 8)}" r="{br}" fill="#06152e" '
               f'opacity=".35"/>')
    out.append(f'<circle cx="{n(bx)}" cy="{n(by)}" r="{br}" fill="url(#ballG{u})"/>')
    out.append(ball_lines(bx, by, br - 1, "#2a0610", 3.2))
    out.append(f'<circle cx="{n(bx)}" cy="{n(by)}" r="{br}" fill="none" stroke="#2a0610" '
               f'stroke-width="3"/>')
    out.append(f'<ellipse cx="{n(bx - br * .38)}" cy="{n(by - br * .42)}" rx="{n(br * .26)}" '
               f'ry="{n(br * .14)}" fill="#ffffff" opacity=".45"/>')
    # net, hanging from the rim and narrowing
    top_l, top_r = rim_cx - rim_rx + 4, rim_cx + rim_rx - 4
    bot_y = rim_cy + 66
    bot_l, bot_r = rim_cx - rim_rx * .55, rim_cx + rim_rx * .55
    net = []
    k = 8
    for i in range(k + 1):
        t = i / k
        xa = top_l + (top_r - top_l) * t
        xb = bot_l + (bot_r - bot_l) * t
        net.append(f"M{n(xa)} {n(rim_cy + 4)}Q{n((xa + xb) / 2 + (t - .5) * 10)} "
                   f"{n((rim_cy + bot_y) / 2)} {n(xb)} {n(bot_y)}")
    for j in range(1, 4):
        t = j / 4
        yy = rim_cy + 4 + (bot_y - rim_cy - 4) * t
        xl = top_l + (bot_l - top_l) * t
        xr = top_r + (bot_r - top_r) * t
        net.append(f"M{n(xl)} {n(yy)}Q{n(rim_cx)} {n(yy + 9)} {n(xr)} {n(yy)}")
    out.append(f'<path d="{"".join(net)}" fill="none" stroke="{WHITE}" stroke-width="2.2" '
               f'stroke-linecap="round" opacity=".92"/>')
    # rim, front half, over the ball and the net
    out.append(f'<path d="M{n(rim_cx - rim_rx)} {n(rim_cy)}A{rim_rx} {rim_ry} 0 0 0 '
               f'{n(rim_cx + rim_rx)} {n(rim_cy)}" fill="none" stroke="{RED}" '
               f'stroke-width="7" stroke-linecap="round"/>')
    # holo foil: diagonal stripes drifting across the art window
    out.append(f'<g class="foil{u}"><rect x="{x0}" y="{y0}" width="{w + 300}" '
               f'height="{h + 300}" fill="url(#foil{u})" opacity=".26"/></g>')
    out.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" filter="url(#grain{u})" '
               f'opacity=".6"/>')
    return "".join(out)
