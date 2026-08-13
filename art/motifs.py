#!/usr/bin/env python3
"""Shared decorative motifs.

The thirteen-star arc is the 1776 colonies device — a public motif, not a team
mark. It is the only ornament that survived from the jersey this card used to
carry; the jersey and the team logo before it were both removed on purpose.
"""

STAR5 = ("M0,-10 L2.94,-3.09 L9.51,-3.09 L4.05,1.18 "
         "L5.88,8.09 L0,4.0 L-5.88,8.09 L-4.05,1.18 "
         "L-9.51,-3.09 L-2.94,-3.09 Z")


def star_arc(cx, cy, rx, ry, n=13, size=1.0, fill="#ffffff",
             start_deg=-160, end_deg=-20, cls=None):
    """Thirteen stars on an elliptical arc.

    Elliptical, not circular: the arc has to span most of the card's width
    while staying tight to the top, and a circular arc flings the end stars
    far above everything else.

    Placement lives on the wrapping <g> and the animation on the child <path>,
    because a CSS transform animation would otherwise replace the placement
    transform outright and stack all thirteen stars on the origin.
    """
    import math
    out = []
    for i in range(n):
        a = math.radians(start_deg + i * (end_deg - start_deg) / (n - 1))
        sx, sy = cx + rx * math.cos(a), cy + ry * math.sin(a)
        c = f' class="{cls}{i}"' if cls else ""
        out.append(f'<g transform="translate({sx:.2f} {sy:.2f}) scale({size:.3f})">'
                   f'<path{c} d="{STAR5}" fill="{fill}"/></g>')
    return "".join(out)
