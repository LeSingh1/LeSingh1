#!/usr/bin/env python3
"""The official Philadelphia 76ers primary logo, inlined as vector paths.

Source: Wikimedia Commons, `Philadelphia_76ers_logo.svg`. It is the real mark,
not a redrawing — earlier attempts at approximating the swoosh 7 by hand were
not close enough to pass.

The 76ers name and logo are trademarks of the Philadelphia 76ers / NBA. This
is fan use on a personal profile page.

The file is self-contained: plain <path>/<polygon>/<circle> with literal fills,
no <style>, no external references, no ids to collide with the host document.
That means the body can be dropped straight into another SVG inside a <g>.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "logo", "Philadelphia_76ers_logo.svg")

# Official team colours, taken from the logo file itself rather than guessed.
BLUE = "#1d428a"
RED = "#c8102e"
WHITE = "#ffffff"

_BODY = None
_VB = None


def _load():
    global _BODY, _VB
    if _BODY is not None:
        return
    raw = open(SRC).read()
    m = re.search(r'viewBox="([\d.\s-]+)"', raw)
    _VB = [float(v) for v in m.group(1).split()]
    body = raw[raw.index(">", raw.index("<svg")) + 1: raw.rindex("</svg>")]
    # Drop metadata blocks; keep only drawable elements.
    body = re.sub(r"<metadata>.*?</metadata>", "", body, flags=re.S)
    body = re.sub(r"<defs>\s*</defs>", "", body, flags=re.S)
    _BODY = body.strip()


def size():
    _load()
    return _VB[2], _VB[3]


def badge(cx, cy, diameter, cls=None):
    """The full circular logo, centred on (cx, cy) at the given diameter."""
    _load()
    w, h = _VB[2], _VB[3]
    s = diameter / w
    c = f' class="{cls}"' if cls else ""
    return (f'<g{c} transform="translate({cx - diameter/2:.2f} {cy - diameter/2:.2f}) '
            f'scale({s:.6f})">{_BODY}</g>')


STAR5 = ("M0,-10 L2.94,-3.09 L9.51,-3.09 L4.05,1.18 "
         "L5.88,8.09 L0,4.0 L-5.88,8.09 L-4.05,1.18 "
         "L-9.51,-3.09 L-2.94,-3.09 Z")
