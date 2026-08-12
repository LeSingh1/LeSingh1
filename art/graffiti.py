#!/usr/bin/env python3
"""Graffiti / screenprint texture primitives.

Deterministic: everything is driven by a seeded PRNG at build time, so the
committed SVGs are stable and diffs stay readable.
"""
import math
import random

RED = "#ED174C"
BLUE = "#006BB6"
NAVY = "#002B5C"
WHITE = "#FFFFFF"


def rng(seed):
    return random.Random(seed)


def filters(uid):
    """Rough-edge, spray and grain filters."""
    return f"""
    <filter id="rough{uid}" x="-15%" y="-15%" width="130%" height="130%">
      <feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves="4" seed="3" result="t"/>
      <feDisplacementMap in="SourceGraphic" in2="t" scale="14"
                         xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <filter id="ragged{uid}" x="-15%" y="-15%" width="130%" height="130%">
      <feTurbulence type="fractalNoise" baseFrequency="0.055" numOctaves="5" seed="9" result="t"/>
      <feDisplacementMap in="SourceGraphic" in2="t" scale="7"
                         xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <filter id="spray{uid}" x="-30%" y="-30%" width="160%" height="160%">
      <feTurbulence type="fractalNoise" baseFrequency="0.42" numOctaves="3" seed="21" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="26"
                         xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <filter id="grain{uid}" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" seed="7" result="n"/>
      <feColorMatrix in="n" type="saturate" values="0"/>
      <feComponentTransfer><feFuncA type="linear" slope="0.09"/></feComponentTransfer>
    </filter>"""


def patterns(uid, dot=WHITE, op="0.13"):
    return f"""
    <pattern id="dots{uid}" width="10" height="10" patternUnits="userSpaceOnUse">
      <circle cx="2.5" cy="2.5" r="2.0" fill="{dot}" opacity="{op}"/>
    </pattern>
    <pattern id="dotsL{uid}" width="17" height="17" patternUnits="userSpaceOnUse">
      <circle cx="4" cy="4" r="3.4" fill="{dot}" opacity="{op}"/>
    </pattern>
    <pattern id="slash{uid}" width="14" height="14" patternUnits="userSpaceOnUse"
             patternTransform="rotate(-40)">
      <rect width="5.5" height="14" fill="{dot}" opacity="0.28"/>
    </pattern>"""


def blob(cx, cy, rx, ry, seed, fill=WHITE, opacity=1.0, points=13, uid=""):
    """A rough brush blob — the grey mass the logo sits on in the poster."""
    r = rng(seed)
    pts = []
    for i in range(points):
        a = 2 * math.pi * i / points
        k = 1 + r.uniform(-0.26, 0.26)
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    d = f"M {pts[0][0]:.1f},{pts[0][1]:.1f} "
    for i in range(points):
        p0 = pts[i]
        p1 = pts[(i + 1) % points]
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        d += f"Q {p0[0]:.1f},{p0[1]:.1f} {mx:.1f},{my:.1f} "
    d += "Z"
    f = f' filter="url(#rough{uid})"' if uid else ""
    return f'<path d="{d}" fill="{fill}" opacity="{opacity}"{f}/>'


def splatter(cx, cy, spread, seed, fill=RED, n=16, rmin=2, rmax=13,
             opacity=0.9, uid=""):
    """A burst of thrown paint.

    Perfect circles read as a dot pattern. Thrown paint travels, so the blobs
    are ellipses stretched along their flight line, each trailing a couple of
    smaller satellites.
    """
    r = rng(seed)
    out = []
    for _ in range(n):
        a = r.uniform(0, 2 * math.pi)
        d = r.uniform(0, 1) ** 0.6 * spread
        px, py = cx + d * math.cos(a), cy + d * math.sin(a)
        rad = max(0.8, r.uniform(rmin, rmax) * (1 - 0.55 * d / spread))
        stretch = 1 + (d / spread) * r.uniform(0.3, 1.5)
        deg = math.degrees(a)
        out.append(f'<ellipse cx="0" cy="0" rx="{rad*stretch:.1f}" ry="{rad:.1f}" '
                   f'transform="translate({px:.1f} {py:.1f}) rotate({deg:.0f})"/>')
        for _ in range(r.randint(0, 2)):        # satellites, thrown further out
            sd = d + r.uniform(rad, rad * 5)
            sa = a + r.uniform(-0.28, 0.28)
            out.append(f'<circle cx="{cx + sd*math.cos(sa):.1f}" '
                       f'cy="{cy + sd*math.sin(sa):.1f}" '
                       f'r="{max(0.5, rad*r.uniform(0.10, 0.30)):.1f}"/>')
    f = f' filter="url(#spray{uid})"' if uid else ""
    return f'<g fill="{fill}" opacity="{opacity}"{f}>{"".join(out)}</g>'


def drips(x, y, w, seed, fill=RED, n=5, lo=18, hi=95, cls=None):
    """Paint runs falling off an edge. Each ends in a fat bead."""
    r = rng(seed)
    out = []
    for i in range(n):
        dx = x + r.uniform(0, w)
        ln = r.uniform(lo, hi)
        wd = r.uniform(3.5, 9)
        c = f' class="{cls}"' if cls else ""
        out.append(
            f'<g{c}><rect x="{dx:.1f}" y="{y:.1f}" width="{wd:.1f}" height="{ln:.1f}" '
            f'rx="{wd/2:.1f}" fill="{fill}"/>'
            f'<circle cx="{dx + wd/2:.1f}" cy="{y + ln:.1f}" r="{wd*0.78:.1f}" fill="{fill}"/></g>')
    return "".join(out)


def brush_stroke(x1, y1, x2, y2, thick, seed, fill=WHITE, opacity=1.0, uid="",
                 overspray=True):
    """A single spray stroke.

    A bare displaced polygon reads as torn paper, not paint. What sells it is
    the halo: a real spray can throws a scatter of droplets along the edge of
    the stroke, densest near the core and thinning outward. So the stroke is
    drawn as a tapered body plus that halo.
    """
    r = rng(seed)
    dx, dy = x2 - x1, y2 - y1
    ln = math.hypot(dx, dy) or 1
    ux, uy = dx / ln, dy / ln
    nx, ny = -uy, ux
    steps = 11
    top, bot = [], []
    for i in range(steps + 1):
        t = i / steps
        px, py = x1 + dx * t, y1 + dy * t
        # sin envelope tapers both ends the way a stroke lifts off
        k = thick * (0.5 + r.uniform(-0.13, 0.13)) * math.sin(math.pi * t) ** 0.62
        top.append((px + nx * k, py + ny * k))
        bot.append((px - nx * k, py - ny * k))
    d = "M " + " L ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in top)
    d += " L " + " L ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in reversed(bot)) + " Z"
    f = f' filter="url(#ragged{uid})"' if uid else ""
    out = [f'<path d="{d}" fill="{fill}" opacity="{opacity}"{f}/>']

    if overspray:
        halo = []
        for _ in range(int(ln / 5)):
            t = r.uniform(0.02, 0.98)
            px, py = x1 + dx * t, y1 + dy * t
            env = thick * math.sin(math.pi * t) ** 0.62
            off = r.gauss(0, 1) * env * 0.85
            if abs(off) < env * 0.45:          # inside the body, no point
                continue
            rad = max(0.5, r.uniform(0.6, 2.4) * (1 - min(1, abs(off) / (env * 2.2))))
            halo.append(f'<circle cx="{px + nx*off:.1f}" cy="{py + ny*off:.1f}" '
                        f'r="{rad:.1f}"/>')
        if halo:
            out.append(f'<g fill="{fill}" opacity="{opacity*0.55:.2f}">{"".join(halo)}</g>')
    return "".join(out)


def tag(x, y, scale, seed, fill=WHITE, opacity=0.9, width=6.0):
    """A hand-thrown spray signature — one continuous looping stroke."""
    r = rng(seed)
    pts = [(0, 0)]
    px, py = 0.0, 0.0
    for i in range(7):
        px += r.uniform(16, 30)
        py = r.uniform(-20, 8) if i % 2 == 0 else r.uniform(4, 26)
        pts.append((px, py))
    d = f"M {pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(1, len(pts)):
        x0, y0 = pts[i - 1]
        x1_, y1_ = pts[i]
        c1x = x0 + (x1_ - x0) * 0.35
        c1y = y0 + r.uniform(-22, 22)
        c2x = x0 + (x1_ - x0) * 0.7
        c2y = y1_ + r.uniform(-22, 22)
        d += f" C {c1x:.1f},{c1y:.1f} {c2x:.1f},{c2y:.1f} {x1_:.1f},{y1_:.1f}"
    return (f'<g transform="translate({x} {y}) scale({scale})" opacity="{opacity}">'
            f'<path d="{d}" fill="none" stroke="{fill}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round"/></g>')


def speckle(x, y, w, h, seed, n=110, fill=WHITE, opacity=0.5, rmax=2.6):
    """Fine overspray."""
    r = rng(seed)
    out = [f'<circle cx="{r.uniform(x, x+w):.1f}" cy="{r.uniform(y, y+h):.1f}" '
           f'r="{r.uniform(0.5, rmax):.1f}"/>' for _ in range(n)]
    return f'<g fill="{fill}" opacity="{opacity}">{"".join(out)}</g>'
