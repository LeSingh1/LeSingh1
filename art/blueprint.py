#!/usr/bin/env python3
"""Drafting primitives for the blueprint artwork.

Everything here returns SVG path data or SVG markup as strings. Nothing is
random, so the committed SVGs are byte-for-byte reproducible.

The one idea worth knowing before editing: a Sheet keeps two copies of every
line that draws itself on. The "pencil" copy is a single faint path that is
always visible. The "ink" copy draws over it with stroke-dashoffset. A frame
frozen at t=0 (a thumbnailer, a slow device) still shows the whole drawing in
pencil, and the finished frame shows it in ink. Type never starts at zero
opacity either; it inks up from a faint ghost.
"""
import math

from text2path import load, text_path

DIN_COND = load("/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf")
DIN_ALT = load("/System/Library/Fonts/Supplemental/DIN Alternate Bold.ttf")
MONO = load("/System/Library/Fonts/Menlo.ttc", 1)        # Menlo Bold

# Two palettes, tuned for contrast on their own backgrounds.
PALETTES = {
    "dark": dict(
        page="#0a1628", panel="#0d1d36", grid="#7cc4ff",
        line="#7cc4ff", accent="#ffb547", ink="#eaf2fc", muted="#8fb3d9",
        minor=".055", major=".13", pencil=".2", hatch=".55"),
    "light": dict(
        page="#f7f9fc", panel="#ffffff", grid="#1f4fa0",
        line="#1f4fa0", accent="#d9480f", ink="#0f1b2d", muted="#4a6587",
        minor=".06", major=".14", pencil=".18", hatch=".5"),
}


def n(v):
    """Compact number formatting for path data."""
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


# ---------------------------------------------------------------- geometry
def line(x1, y1, x2, y2):
    return f"M{n(x1)} {n(y1)}L{n(x2)} {n(y2)}"


def poly(pts, close=True):
    d = "M" + "L".join(f"{n(x)} {n(y)}" for x, y in pts)
    return d + ("Z" if close else "")


def rect(x, y, w, h, r=0.0):
    if not r:
        return poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)])
    return (f"M{n(x + r)} {n(y)}H{n(x + w - r)}"
            f"A{n(r)} {n(r)} 0 0 1 {n(x + w)} {n(y + r)}V{n(y + h - r)}"
            f"A{n(r)} {n(r)} 0 0 1 {n(x + w - r)} {n(y + h)}H{n(x + r)}"
            f"A{n(r)} {n(r)} 0 0 1 {n(x)} {n(y + h - r)}V{n(y + r)}"
            f"A{n(r)} {n(r)} 0 0 1 {n(x + r)} {n(y)}Z")


def circle(cx, cy, r):
    return (f"M{n(cx - r)} {n(cy)}A{n(r)} {n(r)} 0 1 0 {n(cx + r)} {n(cy)}"
            f"A{n(r)} {n(r)} 0 1 0 {n(cx - r)} {n(cy)}Z")


def arc(cx, cy, r, a0, a1):
    """Circular arc from angle a0 to a1 (degrees, clockwise in screen space)."""
    x0 = cx + r * math.cos(math.radians(a0))
    y0 = cy + r * math.sin(math.radians(a0))
    x1 = cx + r * math.cos(math.radians(a1))
    y1 = cy + r * math.sin(math.radians(a1))
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return f"M{n(x0)} {n(y0)}A{n(r)} {n(r)} 0 {large} 1 {n(x1)} {n(y1)}"


def arrowhead(tx, ty, ang, length=13.0, half=3.6):
    """Filled arrowhead with its tip at (tx, ty), pointing along `ang` deg."""
    a = math.radians(ang)
    bx, by = tx - length * math.cos(a), ty - length * math.sin(a)
    px, py = -math.sin(a) * half, math.cos(a) * half
    return poly([(tx, ty), (bx + px, by + py), (bx - px, by - py)])


def hatch(x0, y0, x1, y1, step=7.0):
    """45-degree section lines filling a rectangle."""
    out = []
    k = x0 + y0 + step
    while k < x1 + y1:
        xa, xb = max(x0, k - y1), min(x1, k - y0)
        if xb > xa:
            out.append(line(xa, k - xa, xb, k - xb))
        k += step
    return "".join(out)


def center_cross(cx, cy, r):
    """The small cross that marks a hole centre."""
    return line(cx - r, cy, cx + r, cy) + line(cx, cy - r, cx, cy + r)


# ---------------------------------------------------------------- type
def measure(font, text, size, tracking=0.0):
    return text_path(font, text, size, tracking)[1]


def fit(font, text, size, max_w, tracking=0.0, floor=8.0):
    """Shrink a string until it clears the space actually available."""
    while size > floor:
        d, w = text_path(font, text, size, tracking)
        if w <= max_w:
            return d, w, size
        size -= 0.5
    d, w = text_path(font, text, size, tracking)
    return d, w, size


def wrap(font, text, size, max_w, tracking=0.0):
    """Greedy word wrap on measured widths."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if cur and measure(font, trial, size, tracking) > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- sheet
class Sheet:
    """Collects markup for one SVG, plus the pencil underlay and the CSS.

    ink()  : a stroke that draws itself on, over a faint pencil copy
    fade() : anything else that should arrive in sequence; starts as a ghost
    """

    def __init__(self, uid, W, H, pal, label):
        self.uid, self.W, self.H, self.p, self.label = uid, W, H, pal, label
        self.defs, self.back, self.body, self.front = [], [], [], []
        self.pencil = []

    # --- line work -------------------------------------------------------
    def ink(self, d, t, dur=0.9, w=2.0, color=None, cap="round", layer=None):
        color = color or self.p["line"]
        self.pencil.append((d, w))
        (layer if layer is not None else self.body).append(
            f'<path class="dr{self.uid}" d="{d}" pathLength="1" fill="none" '
            f'stroke="{color}" stroke-width="{w}" stroke-linecap="{cap}" '
            f'stroke-linejoin="round" '
            f'style="animation-delay:{t:.2f}s;animation-duration:{dur:.2f}s"/>')

    def stroke(self, d, w=1.0, color=None, dash=None, opacity=None, t=None,
               layer=None):
        """A static (or fading) stroke: hidden lines, centre lines, hatch."""
        color = color or self.p["line"]
        attrs = (f'd="{d}" fill="none" stroke="{color}" stroke-width="{w}" '
                 f'stroke-linecap="butt"')
        if dash:
            attrs += f' stroke-dasharray="{dash}"'
        if opacity is not None:
            attrs += f' stroke-opacity="{opacity}"'
        (layer if layer is not None else self.body).append(self._fade(attrs, t))

    def fill(self, d, color=None, t=None, layer=None, opacity=None):
        color = color or self.p["line"]
        attrs = f'd="{d}" fill="{color}"'
        if opacity is not None:
            attrs += f' fill-opacity="{opacity}"'
        (layer if layer is not None else self.body).append(self._fade(attrs, t))

    def _fade(self, attrs, t, tag="path"):
        if t is None:
            return f"<{tag} {attrs}/>"
        return (f'<{tag} class="fd{self.uid}" {attrs} '
                f'style="animation-delay:{t:.2f}s"/>')

    # --- type ------------------------------------------------------------
    def text(self, font, s, size, x, y, color, anchor="start", tracking=0.0,
             max_w=None, t=None, layer=None):
        """Outlined type. Returns the width actually used."""
        if max_w:
            d, w, _ = fit(font, s, size, max_w, tracking)
        else:
            d, w = text_path(font, s, size, tracking)
        if anchor == "middle":
            x -= w / 2
        elif anchor == "end":
            x -= w
        attrs = f'd="{d}" fill="{color}" transform="translate({n(x)} {n(y)})"'
        (layer if layer is not None else self.body).append(self._fade(attrs, t))
        return w

    # --- composition -----------------------------------------------------
    def grid(self, x, y, w, h):
        u, p = self.uid, self.p
        minor = "".join(f"M{i} 0V100M0 {i}H100" for i in (20, 40, 60, 80))
        self.defs.append(
            f'<pattern id="g{u}" width="100" height="100" '
            f'patternUnits="userSpaceOnUse" x="{n(x)}" y="{n(y)}">'
            f'<path d="{minor}" stroke="{p["grid"]}" stroke-opacity="{p["minor"]}" '
            f'stroke-width="1" fill="none"/>'
            f'<path d="M0 0V100M0 0H100" stroke="{p["grid"]}" '
            f'stroke-opacity="{p["major"]}" stroke-width="1" fill="none"/>'
            f'</pattern>')
        self.back.append(f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" '
                         f'height="{n(h)}" fill="url(#g{u})"/>')

    def render(self, extra_css=""):
        u, p = self.uid, self.p
        css = f"""
      @keyframes draw{u} {{ from {{ stroke-dashoffset: 1 }} to {{ stroke-dashoffset: 0 }} }}
      @keyframes ink{u} {{ from {{ opacity: .16 }} to {{ opacity: 1 }} }}
      .dr{u} {{ stroke-dasharray: 1 1; animation: draw{u} .9s cubic-bezier(.6,0,.25,1) both }}
      .fd{u} {{ animation: ink{u} .55s ease-out both }}
      {extra_css}
      @media (prefers-reduced-motion: reduce) {{
        .dr{u}, .fd{u}, .cr{u} {{ animation: none !important }}
      }}"""
        # One faint path per stroke width keeps the underlay compact.
        widths = {}
        for d, w in self.pencil:
            widths.setdefault(w, []).append(d)
        pencil = "".join(
            f'<path class="pencil" d="{"".join(ds)}" fill="none" '
            f'stroke="{p["line"]}" stroke-opacity="{p["pencil"]}" '
            f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
            for w, ds in sorted(widths.items()))
        out = [f'<svg width="{self.W}" height="{self.H}" '
               f'viewBox="0 0 {self.W} {self.H}" '
               f'xmlns="http://www.w3.org/2000/svg" role="img" '
               f'aria-label="{self.label}">',
               f"<title>{self.label}</title>",
               f'<defs>{"".join(self.defs)}<style><![CDATA[{css}\n    ]]></style></defs>',
               f'<rect width="{self.W}" height="{self.H}" fill="{p["page"]}"/>']
        out += self.back
        out.append(pencil)
        out += self.body
        out += self.front
        out.append("</svg>")
        return "\n".join(out)
