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
             start_deg=-158, end_deg=-22, cls=None):
    """Thirteen stars spaced evenly ALONG an elliptical arc.

    Elliptical, not circular: the arc has to span most of the card's width
    while staying tight to the top, and a circular arc flings the end stars
    far above everything else.

    The spacing is the subtle part. Stepping uniformly in *angle* looks
    correct on a circle but is badly wrong on a wide ellipse — near the ends
    a degree of angle covers very little horizontal distance, so the stars
    bunch up there and spread out across the top. So walk the curve, measure
    real arc length, and drop a star every total/(n-1) units. That is what
    makes it read as a crown instead of a queue.

    Placement lives on the wrapping <g> and the animation on the child <path>,
    because a CSS transform animation would otherwise replace the placement
    transform outright and stack all thirteen stars on the origin.
    """
    import math

    a0, a1 = math.radians(start_deg), math.radians(end_deg)

    def pt(t):
        a = a0 + (a1 - a0) * t
        return cx + rx * math.cos(a), cy + ry * math.sin(a)

    # cumulative arc length over a dense sampling of the curve
    STEPS = 800
    cum = [0.0]
    px, py = pt(0.0)
    for i in range(1, STEPS + 1):
        qx, qy = pt(i / STEPS)
        cum.append(cum[-1] + math.hypot(qx - px, qy - py))
        px, py = qx, qy
    total = cum[-1]

    def t_at(length):
        """Invert the arc-length table."""
        lo, hi = 0, STEPS
        while lo < hi:
            mid = (lo + hi) // 2
            if cum[mid] < length:
                lo = mid + 1
            else:
                hi = mid
        if lo == 0:
            return 0.0
        prev, cur = cum[lo - 1], cum[lo]
        frac = 0.0 if cur == prev else (length - prev) / (cur - prev)
        return (lo - 1 + frac) / STEPS

    out = []
    for i in range(n):
        sx, sy = pt(t_at(total * i / (n - 1)))
        c = f' class="{cls}{i}"' if cls else ""
        out.append(f'<g transform="translate({sx:.2f} {sy:.2f}) scale({size:.3f})">'
                   f'<path{c} d="{STAR5}" fill="{fill}"/></g>')
    return "".join(out)
