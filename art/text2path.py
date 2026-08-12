#!/usr/bin/env python3
"""Convert a text string into an SVG path using a real font file.

Used so the README artwork carries Caslon everywhere, not just on machines
that happen to have it installed. GitHub renders README SVGs inside <img>,
which blocks webfont loading — vector outlines are the only guarantee.
"""
import sys, json, argparse
from fontTools.ttLib import TTFont, TTCollection
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform


def load(path, index=0):
    if path.lower().endswith(".ttc"):
        return TTCollection(path).fonts[index]
    return TTFont(path)


def text_path(font, text, size, letter_spacing=0.0, cap_align=False):
    """Return (path_d, advance_width). Baseline sits at y=0, glyphs go up (-y)."""
    upm = font["head"].unitsPerEm
    scale = size / upm
    cmap = font.getBestCmap()
    gs = font.getGlyphSet()
    hmtx = font["hmtx"]

    # kerning from the legacy 'kern' table when present
    kern = {}
    if "kern" in font:
        for st in font["kern"].kernTables:
            kern.update(st.kernTable)

    x = 0.0
    parts = []
    prev = None
    for ch in text:
        gname = cmap.get(ord(ch))
        if gname is None:
            x += size * 0.35 + letter_spacing
            prev = None
            continue
        if prev is not None:
            x += kern.get((prev, gname), 0) * scale
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
        tpen = TransformPen(pen, Transform(scale, 0, 0, -scale, x, 0))
        gs[gname].draw(tpen)
        d = pen.getCommands()
        if d:
            parts.append(d)
        x += hmtx[gname][0] * scale + letter_spacing
        prev = gname
    if parts:
        x -= letter_spacing
    return " ".join(parts), x


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--font", required=True)
    ap.add_argument("--index", type=int, default=0)
    ap.add_argument("--size", type=float, required=True)
    ap.add_argument("--tracking", type=float, default=0.0, help="letter spacing in px")
    ap.add_argument("text", nargs="+")
    a = ap.parse_args()
    f = load(a.font, a.index)
    out = []
    for t in a.text:
        d, w = text_path(f, t, a.size, a.tracking)
        out.append({"text": t, "d": d, "width": round(w, 2)})
    print(json.dumps(out, indent=None))


if __name__ == "__main__":
    main()
