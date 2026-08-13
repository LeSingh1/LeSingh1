#!/usr/bin/env python3
"""An original basketball jersey, drawn from scratch.

This replaces the team logo on the card. The palette stays — Philadelphia
blue and red — but every shape here is original, so the artwork carries no
trademark. A jersey is also the more honest centrepiece for a rookie card:
it is his name and his number, not a borrowed badge.

Drawn around the origin: x is centred, y runs 0 (shoulders) to 240 (hem).
"""

BLUE = "#1d428a"
RED = "#c8102e"
WHITE = "#ffffff"

# Sleeveless jersey: shoulder line, a scooped neck notch, deep armholes,
# a body that narrows at the waist and flares slightly to the hem.
BODY = (
    "M -78,16 "
    "C -52,4 -34,0 -26,2 "
    "C -22,26 -14,37 0,37 "
    "C 14,37 22,26 26,2 "
    "C 34,0 52,4 78,16 "
    "C 86,42 82,60 72,76 "
    "C 54,86 46,104 49,130 "
    "L 57,238 "
    "C 20,246 -20,246 -57,238 "
    "L -49,130 "
    "C -46,104 -54,86 -72,76 "
    "C -82,60 -86,42 -78,16 "
    "Z"
)

# Trim runs: neck scoop, both armholes, hem.
NECK = "M -26,2 C -22,26 -14,37 0,37 C 14,37 22,26 26,2"
ARM_L = "M -72,76 C -54,86 -46,104 -49,130"
ARM_R = "M 72,76 C 54,86 46,104 49,130"
HEM = "M -57,238 C -20,246 20,246 57,238"

ARC_OVERHANG = 0.135   # how far the star arc rises above the shoulders

STAR5 = ("M0,-10 L2.94,-3.09 L9.51,-3.09 L4.05,1.18 "
         "L5.88,8.09 L0,4.0 L-5.88,8.09 L-4.05,1.18 "
         "L-9.51,-3.09 L-2.94,-3.09 Z")


def star_arc(cx, cy, rx, ry, n=13, size=1.0, fill=WHITE,
             start_deg=-160, end_deg=-20, cls=None):
    """Thirteen stars — one per original colony, not a team device."""
    import math
    out = []
    for i in range(n):
        a = math.radians(start_deg + i * (end_deg - start_deg) / (n - 1))
        sx, sy = cx + rx * math.cos(a), cy + ry * math.sin(a)
        c = f' class="{cls}{i}"' if cls else ""
        out.append(f'<g transform="translate({sx:.2f} {sy:.2f}) scale({size:.3f})">'
                   f'<path{c} d="{STAR5}" fill="{fill}"/></g>')
    return "".join(out)


def jersey(cx, cy, height, name_paths=None, number_paths=None,
           body=BLUE, trim=RED, ink=WHITE, star_cls=None, uid=""):
    """A jersey centred on (cx, cy) at the given height.

    name_paths / number_paths are (path_d, width) pairs measured by the
    caller, so the type is fitted rather than guessed at.
    """
    s = height / 240.0
    out = [f'<g transform="translate({cx} {cy - height/2:.2f}) scale({s:.5f})">']
    out.append(f'<g transform="translate(0 0)">')

    # shadow, so it reads as cloth hanging off the card rather than a sticker
    out.append(f'<path d="{BODY}" fill="#000000" opacity=".28" '
               f'transform="translate(5 7)"/>')
    out.append(f'<path d="{BODY}" fill="{body}"/>')

    # trim: a heavy white run with a thin red keyline inside it
    for d in (NECK, ARM_L, ARM_R, HEM):
        out.append(f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="9" '
                   f'stroke-linecap="round"/>')
        out.append(f'<path d="{d}" fill="none" stroke="{trim}" stroke-width="3.2" '
                   f'stroke-linecap="round"/>')

    # Side panels: narrow strips hugging the outer seam. Wide ones read as
    # a red jersey with a blue stripe down the middle.
    out.append(f'<path d="M -46,146 L -57,238 C -53,239.4 -48,240.6 -43,241.5 '
               f'L -34,147 Z" fill="{trim}"/>')
    out.append(f'<path d="M 46,146 L 57,238 C 53,239.4 48,240.6 43,241.5 '
               f'L 34,147 Z" fill="{trim}"/>')

    if name_paths:
        d, w = name_paths
        out.append(f'<path d="{d}" fill="{trim}" opacity=".5" '
                   f'transform="translate({-w/2 + 2:.1f} 106)"/>')
        out.append(f'<path d="{d}" fill="{ink}" transform="translate({-w/2:.1f} 104)"/>')
    if number_paths:
        d, w = number_paths
        out.append(f'<path d="{d}" fill="{trim}" transform="translate({-w/2 + 3:.1f} 206)" '
                   f'opacity=".55"/>')
        out.append(f'<path d="{d}" fill="{ink}" transform="translate({-w/2:.1f} 203)"/>')

    out.append("</g>")
    if star_cls is not None:
        out.append(star_arc(0, 22, 108, 46, size=0.95, fill=ink, cls=star_cls))
    out.append("</g>")
    return "".join(out)
