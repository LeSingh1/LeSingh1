#!/usr/bin/env python3
"""Generate the profile artwork: a blueprint drawing sheet.

The hero is an engineering drawing of an original two-finger robot gripper
holding a ball, with a title block, a revision block, notes and a detail view.
Its dimension callouts carry the real numbers from stats.py. The section
strips use the same drafting language.

Rules, each learned by breaking it (see art/README.md):

1. Every glyph is a vector outline. GitHub shows README images inside <img>,
   and an <img> cannot load a webfont.
2. Never put a CSS transform animation on an element that also has an SVG
   transform attribute. This artwork animates only stroke-dashoffset and
   opacity, so the question never comes up, and a test keeps it that way.
3. A frozen frame must still read. Lines draw on over a pencil underlay and
   type inks up from a ghost, so t=0 shows the whole drawing faintly.
4. Text is fitted, never hardcoded. fit() shrinks a string until it clears
   the space it actually has.
"""
import math
import os

import blueprint as B
import stats as ST
from blueprint import DIN_ALT, DIN_COND, MONO

OUT = os.path.dirname(os.path.abspath(__file__))
THEME = {}


def set_theme(dark):
    THEME.clear()
    THEME.update(B.PALETTES["dark" if dark else "light"], dark=dark)


# =========================================================================
# HERO: the drawing sheet
# =========================================================================
HERO_W, HERO_H = 1200, 720
FRAME = (34, 34, 1166, 686)          # inner border x0, y0, x1, y1
CX = 400                              # gripper axis

HERO_LABEL = (
    f"Engineering drawing of a two-finger robot gripper holding a ball. "
    f"Title block: Shaurya Singh. Dimension callouts: {ST.MERGES} merged pull "
    f"requests, {ST.ORGS} organizations, {ST.REPOS} repositories, "
    f"{ST.WINS} hackathon wins. Detail A shows a planned contact microphone "
    f"on the fingertip.")


def sheet_frame(S):
    """Outer trim line, inner border, zone markers and centring marks."""
    p = S.p
    x0, y0, x1, y1 = FRAME
    W, H = S.W, S.H
    S.stroke(B.rect(12, 12, W - 24, H - 24), w=1, color=p["line"], opacity=".55",
             layer=S.back)
    S.stroke(B.rect(x0, y0, x1 - x0, y1 - y0), w=2.2, color=p["line"],
             layer=S.back)
    cols, rows = 6, 4
    cw, rh = (x1 - x0) / cols, (y1 - y0) / rows
    ticks = []
    for i in range(1, cols):
        x = x0 + cw * i
        ticks.append(B.line(x, 12, x, y0) + B.line(x, y1, x, H - 12))
    for i in range(1, rows):
        y = y0 + rh * i
        ticks.append(B.line(12, y, x0, y) + B.line(x1, y, W - 12, y))
    S.stroke("".join(ticks), w=1, color=p["line"], opacity=".55", layer=S.back)
    for i in range(cols):
        x = x0 + cw * (i + 0.5)
        lab = str(cols - i)        # drawings number zones right to left
        for yb in (28, H - 16):
            S.text(DIN_COND, lab, 13, x, yb, p["muted"], anchor="middle",
                   layer=S.back)
    for i in range(rows):
        y = y0 + rh * (i + 0.5) + 5
        lab = "DCBA"[i]
        for xc in (23, W - 23):
            S.text(DIN_COND, lab, 13, xc, y, p["muted"], anchor="middle",
                   layer=S.back)
    # centring marks: small solid triangles at the middle of each edge
    m = []
    for x in (W / 2,):
        m.append(B.poly([(x - 6, 12), (x + 6, 12), (x, y0 - 4)]))
        m.append(B.poly([(x - 6, H - 12), (x + 6, H - 12), (x, y1 + 4)]))
    for y in (H / 2,):
        m.append(B.poly([(12, y - 6), (12, y + 6), (x0 - 4, y)]))
        m.append(B.poly([(W - 12, y - 6), (W - 12, y + 6), (x1 + 4, y)]))
    S.fill("".join(m), color=p["line"], layer=S.back)


def callout_inline(S, cx, y, num, label, t):
    """Number + label set in one line, centred on (cx, y). Returns half-width."""
    p = S.p
    dn, wn = B.text_path(DIN_ALT, num, 34)
    dl, wl = B.text_path(DIN_COND, label, 19, 1.6)
    gap = 9
    total = wn + gap + wl
    x = cx - total / 2
    base = y + 12
    S.body.append(S._fade(f'd="{dn}" fill="{p["accent"]}" '
                          f'transform="translate({B.n(x)} {B.n(base)})"', t))
    S.body.append(S._fade(f'd="{dl}" fill="{p["ink"]}" '
                          f'transform="translate({B.n(x + wn + gap)} {B.n(base)})"',
                          t + 0.12))
    return total / 2


def callout_stacked(S, cx, cy, num, label, t):
    """Number over label, centred on (cx, cy). Returns (half-height)."""
    p = S.p
    S.text(DIN_ALT, num, 36, cx, cy - 2, p["accent"], anchor="middle", t=t)
    S.text(DIN_COND, label, 19, cx, cy + 22, p["ink"], anchor="middle",
           tracking=1.6, t=t + 0.12)
    return 36


def dim_vertical(S, x, y1, y2, ext1, ext2, num, label, t):
    """Vertical dimension at x. ext1/ext2 are the x the extension lines
    start from at y1 and y2."""
    sgn = 1 if x > ext1 else -1
    S.ink(B.line(ext1 + 4 * sgn, y1, x + 8 * sgn, y1), t, 0.5, w=1.1)
    S.ink(B.line(ext2 + 4 * sgn, y2, x + 8 * sgn, y2), t + .05, 0.5, w=1.1)
    cy = (y1 + y2) / 2
    callout_stacked(S, x, cy, num, label, t + 0.45)
    S.ink(B.line(x, cy - 40, x, y1 + 2), t + 0.2, 0.55, w=1.1)
    S.ink(B.line(x, cy + 34, x, y2 - 2), t + 0.2, 0.55, w=1.1)
    S.fill(B.arrowhead(x, y1, -90) + B.arrowhead(x, y2, 90), t=t + 0.6)


def gripper(S):
    """The centrepiece: an original two-finger parallel gripper on a ball."""
    p = S.p
    L = p["line"]
    # mounting flange and palm
    S.ink(B.rect(350, 120, 100, 24, 3), 0.05, 0.8, w=2.2)
    S.ink(B.rect(230, 144, 340, 100, 9), 0.2, 1.1, w=2.4)
    # carriages riding the palm's rail
    S.ink(B.rect(262, 244, 64, 26, 2), 0.5, 0.7, w=2.2)
    S.ink(B.rect(474, 244, 64, 26, 2), 0.55, 0.7, w=2.2)
    # fingers, with a chamfer on the outer tip
    left = [(272, 270), (312, 270), (312, 518), (290, 518), (272, 500)]
    right = [(2 * CX - x, y) for x, y in left]
    S.ink(B.poly(left), 0.7, 1.0, w=2.4)
    S.ink(B.poly(right), 0.75, 1.0, w=2.4)
    # lightening slots
    S.ink(B.rect(282, 296, 20, 124, 10), 1.0, 0.8, w=1.6)
    S.ink(B.rect(498, 296, 20, 124, 10), 1.05, 0.8, w=1.6)
    # grip pads
    S.ink(B.rect(312, 450, 8, 60), 1.1, 0.5, w=1.8)
    S.ink(B.rect(480, 450, 8, 60), 1.1, 0.5, w=1.8)
    S.stroke(B.hatch(312, 450, 320, 510, 5), w=0.9, opacity=p["hatch"], t=1.5)
    S.stroke(B.hatch(480, 450, 488, 510, 5), w=0.9, opacity=p["hatch"], t=1.5)
    # the ball, with two seams so it reads as a sphere
    S.ink(B.circle(CX, 480, 80), 1.2, 1.1, w=2.4)
    S.ink("M320 480A80 20 0 0 0 480 480", 1.6, 0.7, w=1.3)
    S.ink("M400 400A30 80 0 0 1 400 560", 1.7, 0.7, w=1.3)
    # contact mic: a piezo disc on the right finger (planned, see Detail A)
    S.ink(B.circle(508, 480, 9), 1.8, 0.5, w=1.6)
    S.ink(B.circle(508, 480, 4.5), 1.9, 0.4, w=1.2)
    # holes: flange bolts, palm screws, carriage screws
    holes = [(372, 132, 5), (428, 132, 5),
             (248, 162, 4.5), (552, 162, 4.5), (248, 226, 4.5), (552, 226, 4.5),
             (278, 257, 3.5), (310, 257, 3.5), (490, 257, 3.5), (522, 257, 3.5)]
    for i, (hx, hy, hr) in enumerate(holes):
        S.ink(B.circle(hx, hy, hr), 0.6 + 0.04 * i, 0.4, w=1.3)
    S.stroke("".join(B.center_cross(hx, hy, hr + 4) for hx, hy, hr in holes),
             w=0.8, opacity=".7", t=1.4)
    # hidden lines: lead screw and motor inside the palm
    S.stroke(B.line(262, 188, 538, 188) + B.line(262, 200, 538, 200),
             w=1.2, dash="7 4", t=1.3)
    S.stroke(B.circle(CX, 194, 20), w=1.2, dash="7 4", t=1.35)
    # centre lines: gripper axis and the ball's horizontal
    S.stroke(B.line(CX, 108, CX, 578), w=1, dash="22 4 4 4", t=1.45)
    S.stroke(B.line(326, 480, 474, 480), w=1, dash="22 4 4 4", t=1.5)
    # Detail A boundary on the main view
    S.ink(B.circle(500, 480, 36), 2.0, 0.6, w=1.1)
    S.ink(B.line(526, 455, 546, 436), 2.2, 0.3, w=1.1)
    S.text(DIN_COND, "A", 24, 548, 436, p["ink"], t=2.3)


def dimensions(S):
    p = S.p
    # top: palm width
    x1, x2, y = 230, 570, 92
    S.ink(B.line(x1, 140, x1, y - 8), 2.0, 0.5, w=1.1)
    S.ink(B.line(x2, 140, x2, y - 8), 2.05, 0.5, w=1.1)
    half = callout_inline(S, CX, y, str(ST.ORGS), "ORGANIZATIONS", 2.5)
    S.ink(B.line(CX - half - 12, y, x1 + 2, y), 2.2, 0.55, w=1.1)
    S.ink(B.line(CX + half + 12, y, x2 - 2, y), 2.2, 0.55, w=1.1)
    S.fill(B.arrowhead(x1, y, 180) + B.arrowhead(x2, y, 0), t=2.6)

    # left: finger length
    dim_vertical(S, 168, 270, 518, 272, 290, str(ST.REPOS), "REPOSITORIES", 2.3)
    # right: overall height, flange top to fingertip
    dim_vertical(S, 662, 120, 518, 450, 528, str(ST.WINS), "HACKATHON WINS", 2.6)

    # the ball's diameter: a leader note, the headline number
    a = 58
    tx = CX + 80 * math.cos(math.radians(a))
    ty = 480 + 80 * math.sin(math.radians(a))
    S.ink(B.line(tx + 4, ty + 7, 476, 606) + "H492", 2.9, 0.6, w=1.1)
    S.fill(B.arrowhead(tx, ty, a - 180 + 360), t=3.2)
    S.text(DIN_ALT, f"Ø{ST.MERGES}", 52, 500, 624, p["accent"], t=3.2)
    S.text(DIN_COND, "MERGED PULL REQUESTS", 20, 502, 652, p["ink"],
           tracking=1.8, t=3.35)

    # view label
    S.text(DIN_COND, "FRONT VIEW", 21, 62, 640, p["ink"], tracking=2)
    S.stroke(B.line(62, 647, 62 + B.measure(DIN_COND, "FRONT VIEW", 21, 2), 647),
             w=1.4, color=p["ink"])
    S.text(DIN_COND, "TWO-FINGER GRIPPER  ·  SCALE 1:2", 15, 62, 668,
           p["muted"], tracking=1.2)


def detail_a(S):
    """Detail A at 4:1: the fingertip, the pad, and the planned contact mic."""
    p = S.p
    u = S.uid
    cx, cy, r = 880, 236, 100
    S.defs.append(f'<clipPath id="dc{u}"><circle cx="{cx}" cy="{cy}" r="{r - 1}"/></clipPath>')
    # the panel behind the detail hides the grid, as a cleared drafting area
    S.body.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{p["page"]}"/>')
    S.ink(B.circle(cx, cy, r), 1.9, 1.0, w=1.4)
    # ball surface: circle centre (504,236) r 320, clipped to the detail
    S.ink("M814.9 160.1A320 320 0 0 1 814.9 311.9", 2.3, 0.7, w=2.6)
    # pad faces (x 824 and 856) clipped to the detail circle
    for x, t in ((824, 2.35), (856, 2.45)):
        h = math.sqrt(r * r - (x - cx) ** 2)
        S.ink(B.line(x, cy - h, x, cy + h), t, 0.6, w=2.4)
    S.body.append(f'<g clip-path="url(#dc{u})">')
    S.stroke(B.hatch(824, 120, 856, 352, 8), w=1, opacity=p["hatch"], t=2.6)
    S.body.append("</g>")
    # piezo disc on the finger
    S.ink(B.circle(936, 236, 34), 2.5, 0.6, w=2.2)
    S.ink(B.circle(936, 236, 18), 2.6, 0.5, w=1.4)
    # vibration from the contact patch, travelling toward the mic
    for i, rr in enumerate((16, 30, 44)):
        S.ink(B.arc(824, 236, rr, -38, 38), 2.8 + 0.12 * i, 0.4, w=1.4,
              color=p["accent"])
    # labels
    tx = 1000
    S.text(DIN_COND, "DETAIL A", 28, tx, 172, p["ink"], tracking=2, t=2.4)
    S.text(DIN_COND, "SCALE 4:1", 15, tx, 194, p["muted"], tracking=1.4, t=2.5)
    S.ink(B.line(962, 258, 990, 290) + "H1150", 2.9, 0.6, w=1.1)
    S.fill(B.arrowhead(962, 258, 228), t=3.1)
    S.text(DIN_COND, "CONTACT MIC", 20, tx, 284, p["ink"], tracking=1.6, t=3.0)
    S.text(DIN_COND, "PLANNED, NOT BUILT YET", 15, tx, 310, p["accent"],
           tracking=1.2, t=3.1)


def revision_block(S):
    p = S.p
    x0, x1, y0 = 760, 1166, 34
    S.body.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="58" '
                  f'fill="{p["panel"]}"/>')
    S.stroke(B.rect(x0, y0, x1 - x0, 58) + B.line(x0, y0 + 20, x1, y0 + 20)
             + B.line(x0 + 54, y0, x0 + 54, y0 + 58)
             + B.line(x1 - 110, y0, x1 - 110, y0 + 58), w=1.3)
    for s, x in (("REV", x0 + 27), ("DESCRIPTION", (x0 + 54 + x1 - 110) / 2),
                 ("DATE", x1 - 55)):
        S.text(DIN_COND, s, 12, x, y0 + 15, p["muted"], anchor="middle",
               tracking=1.4)
    S.text(DIN_COND, "D", 22, x0 + 27, y0 + 48, p["accent"], anchor="middle")
    S.text(DIN_COND, "REDRAWN AS A BLUEPRINT", 18, (x0 + 54 + x1 - 110) / 2,
           y0 + 47, p["ink"], anchor="middle", tracking=1.4)
    S.text(DIN_COND, "NOV 2026", 18, x1 - 55, y0 + 47, p["ink"],
           anchor="middle", tracking=1.4)


def notes(S):
    p = S.p
    x, y = 774, 392
    S.text(DIN_COND, "NOTES", 17, x, y, p["accent"], tracking=2.4)
    lines = [("1.", "DIMENSIONS ARE REAL COUNTS FROM GITHUB, NOV 2026."),
             ("2.", "DETAIL A IS THE NEXT PROJECT: CAN A CHEAP CONTACT MIC "
                    "HEAR A ROBOT'S GRIP START TO SLIP?")]
    yy = y + 24
    for num, body in lines:
        S.text(DIN_COND, num, 16, x, yy, p["muted"], tracking=1)
        for ln in B.wrap(DIN_COND, body, 16, 360, 1.0):
            S.text(DIN_COND, ln, 16, x + 20, yy, p["ink"], tracking=1.0)
            yy += 21
    # the one looping detail: a caret blinking after a short command
    cmd = "$ ./listen --for slip"
    w = S.text(MONO, cmd, 15, x, yy + 10, p["accent"])
    S.body.append(f'<rect class="cr{S.uid}" x="{B.n(x + w + 6)}" y="{yy - 3}" '
                  f'width="9" height="16" fill="{p["accent"]}"/>')


def title_block(S):
    p = S.p
    x0, y0, x1, y1 = 760, 514, 1166, 686
    S.body.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" '
                  f'height="{y1 - y0}" fill="{p["panel"]}"/>')
    r1, r2, r3 = y0 + 66, y0 + 98, y0 + 135
    grid = (B.rect(x0, y0, x1 - x0, y1 - y0)
            + B.line(x0, r1, x1, r1) + B.line(x0, r2, x1, r2)
            + B.line(x0, r3, x1, r3))
    c3 = [x0, x0 + 132, x0 + 222, x0 + 302, x1]       # row 3 cells
    c4 = [x0, x0 + 132, x0 + 302, x1]                 # row 4 cells
    for x in c3[1:-1]:
        grid += B.line(x, r2, x, r3)
    for x in c4[1:-1]:
        grid += B.line(x, r3, x, y1)
    S.stroke(grid, w=1.3)
    S.stroke(B.rect(x0, y0, x1 - x0, y1 - y0), w=2.2)

    pad = 12
    S.text(DIN_COND, "NAME", 12, x0 + pad, y0 + 16, p["muted"], tracking=1.4)
    S.text(DIN_ALT, "SHAURYA SINGH", 38, x0 + pad, y0 + 56, p["ink"],
           tracking=2.5, max_w=x1 - x0 - 2 * pad)
    S.text(DIN_COND, "FIXES OPEN SOURCE  ·  DESIGNS ROBOTS  ·  BUILDS AGENTS",
           17, x0 + pad, r1 + 23, p["line"], tracking=1.3,
           max_w=x1 - x0 - 2 * pad)

    def cells(xs, top, bottom, items):
        for (a, b), (lab, val) in zip(zip(xs, xs[1:]), items):
            S.text(DIN_COND, lab, 11, a + 9, top + 13, p["muted"], tracking=1.3)
            S.text(DIN_COND, val, 18, a + 9, bottom - 7, p["ink"], tracking=1.2,
                   max_w=b - a - 16)

    cells(c3, r2, r3, [("DWG NO.", "LS1-2029-01"), ("SCALE", "1:2"),
                       ("REV", "D"), ("SHEET", "1 OF 1")])
    cells(c4, r3, y1, [("DRAWN", "S. SINGH"), ("CHECKED", "TEST_ART.PY"),
                       ("DATE", "NOV 2026")])


def hero():
    p = THEME
    S = B.Sheet("H", HERO_W, HERO_H, p, HERO_LABEL)
    x0, y0, x1, y1 = FRAME
    S.grid(x0, y0, x1 - x0, y1 - y0)
    sheet_frame(S)
    revision_block(S)
    gripper(S)
    dimensions(S)
    detail_a(S)
    notes(S)
    title_block(S)
    caret = (f"@keyframes blink{S.uid} {{ 0%, 55% {{ opacity: 1 }} 56%, 100% {{ opacity: 0 }} }}\n"
             f"      .cr{S.uid} {{ animation: blink{S.uid} 1.1s steps(1) infinite }}")
    return S.render(caret)


# =========================================================================
# SECTION STRIPS
# =========================================================================
RULE_W, RULE_H = 1200, 84


def rule(name, num, title):
    p = THEME
    uid = "R" + name
    S = B.Sheet(uid, RULE_W, RULE_H, p, f"Section {num}: {title}")
    y0, y1 = 12, 72
    x0, x1 = 6, RULE_W - 6
    S.grid(0, 0, RULE_W, RULE_H)
    S.body.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" '
                  f'fill="{p["page"]}" fill-opacity=".72"/>')
    cell = 86
    S.stroke(B.rect(x0, y0, x1 - x0, y1 - y0), w=1.8)
    S.stroke(B.line(x0 + cell, y0, x0 + cell, y1), w=1.4)
    S.text(DIN_ALT, num, 32, x0 + cell / 2, 54, p["accent"], anchor="middle")
    tw = S.text(DIN_COND, title.upper(), 34, x0 + cell + 22, 55, p["ink"],
                tracking=3, max_w=760)

    # a leader runs from the title into a balloon carrying the section letter
    letter = "ABCDEFGH"[int(num) - 1]
    bx, br, ly = x1 - 34, 15, 42
    lx0 = x0 + cell + 22 + tw + 26
    S.fill(B.circle(lx0, ly, 3.2), t=0.1)
    S.ink(B.line(lx0, ly, bx - br, ly), 0.15, 1.1, w=1.2)
    S.ink(B.circle(bx, ly, br), 1.0, 0.5, w=1.5)
    S.text(DIN_COND, letter, 18, bx, ly + 7, p["line"], anchor="middle", t=1.1)
    # scale ticks hanging from the strip's lower edge
    ticks = []
    x = x0 + cell + 10
    i = 0
    while x < x1 - 4:
        h = 9 if i % 5 == 0 else 4.5
        ticks.append(B.line(x, y1, x, y1 - h))
        x += 12
        i += 1
    S.stroke("".join(ticks), w=1, opacity=".5", t=0.4)
    return S.render()


SECTIONS = [
    ("highlights", "01", "Highlights"),
    ("builds", "02", "Featured Builds"),
    ("opensource", "03", "Open Source"),
    ("robotics", "04", "Robotics and Research"),
    ("life", "05", "Off the Keyboard"),
    ("stack", "06", "Toolkit"),
    ("activity", "07", "Contributions"),
    ("contact", "08", "Contact"),
]


def main():
    total = 0
    for dark in (False, True):
        set_theme(dark)
        suf = "-dark" if dark else ""
        files = {f"hero{suf}.svg": hero()}
        for nm, num, title in SECTIONS:
            files[f"rule-{nm}{suf}.svg"] = rule(nm, num, title)
        for fn, body in files.items():
            with open(os.path.join(OUT, fn), "w") as f:
                f.write(body)
            total += len(body)
            print(f"{fn:28} {len(body) / 1024:6.1f} KB")
    print(f"{'total':28} {total / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
