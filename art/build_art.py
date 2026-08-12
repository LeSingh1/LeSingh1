#!/usr/bin/env python3
"""Generate the README artwork.

Design: a 1776 Philadelphia letterpress broadside in 76ers colours.
Dunlap printed the Declaration in Caslon a few blocks from where the
Sixers play; the team is named for the year. So the page is set like a
printed proclamation rather than a dashboard.

Every piece of display type is emitted as vector outlines. GitHub renders
README SVGs inside <img>, which cannot load webfonts, so outlines are the
only way Caslon survives on someone else's machine.
"""
import os
from text2path import load, text_path

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profile", "art")
CASLON = "/System/Library/Fonts/Supplemental/BigCaslon.ttf"
BASKER = "/System/Library/Fonts/Supplemental/Baskerville.ttc"

caslon = load(CASLON)
bask_bold = load(BASKER, 1)
bask_ital = load(BASKER, 2)
bask_reg = load(BASKER, 0)

# ---- 76ers palette, plus paper ------------------------------------------
# Two inkings of the same press. Light is a broadside on laid paper; dark is
# the same forme pulled in cream ink on a slate sheet. Set via set_theme().
LIGHT = dict(
    BLUE="#006BB6", RED="#ED174C", NAVY="#00285E",
    INK="#15120E", PAPER="#F1E9D6", PAPER_D="#E4D8BE", FADE="#8A7C60",
    NOISE="0.055",
)
DARK = dict(
    BLUE="#3B9BE0", RED="#FF3F6E", NAVY="#8FC2F0",
    INK="#EDE3CD", PAPER="#141A22", PAPER_D="#0A0E14", FADE="#7E8CA0",
    NOISE="0.075",
)

BLUE = RED = NAVY = INK = PAPER = PAPER_D = FADE = NOISE = ""


def set_theme(dark: bool):
    g = globals()
    g.update(DARK if dark else LIGHT)


def P(font, text, size, tracking=0.0):
    """(path_d, width) for text rendered as outlines."""
    return text_path(font, text, size, tracking)


def centered(font, text, size, tracking, cx, y, fill, extra=""):
    d, w = P(font, text, size, tracking)
    return (
        f'<path d="{d}" fill="{fill}" transform="translate({cx - w/2:.2f} {y})" {extra}/>',
        w,
    )


def paper_defs(uid, w, h):
    """Laid-paper ground: fibre noise, a warm vignette, and press texture."""
    return f"""
    <filter id="fib{uid}" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" seed="7" result="n"/>
      <feColorMatrix in="n" type="saturate" values="0"/>
      <feComponentTransfer><feFuncA type="linear" slope="{NOISE}"/></feComponentTransfer>
    </filter>
    <filter id="blot{uid}" x="-20%" y="-20%" width="140%" height="140%">
      <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="3" seed="19" result="t"/>
      <feDisplacementMap in="SourceGraphic" in2="t" scale="1.7" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <radialGradient id="vig{uid}" cx="50%" cy="46%" r="72%">
      <stop offset="55%" stop-color="{PAPER}"/>
      <stop offset="100%" stop-color="{PAPER_D}"/>
    </radialGradient>"""


def paper_ground(uid, w, h, r=3):
    return f"""  <rect width="{w}" height="{h}" rx="{r}" fill="url(#vig{uid})"/>
  <rect width="{w}" height="{h}" rx="{r}" filter="url(#fib{uid})" opacity="0.85"/>"""


# =========================================================================
# HERO — the broadside
# =========================================================================
def hero():
    W, H = 1200, 460
    cx = W / 2
    s = []
    s.append(
        f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="Shaurya Singh — builder of agents, Philadelphia 1776 broadside">'
    )
    s.append("<defs>")
    s.append(paper_defs("H", W, H))
    # the two ink plates, offset then registered — a press finding alignment
    s.append(f"""
    <style><![CDATA[
      /* The press cycle: the two colour plates drift into register under the
         black impression. Nothing here animates opacity from zero — if a
         renderer never advances the timeline (a preview card, a thumbnailer,
         an <img> rasterised at t=0) the sheet must still read as finished.
         Motion is the enhancement; the resting state is the artwork. */
      @keyframes registerR {{
        0%      {{ transform: translate(7px, -5px); }}
        55%,100% {{ transform: translate(0,0); }}
      }}
      @keyframes registerB {{
        0%      {{ transform: translate(-8px, 6px); }}
        62%,100% {{ transform: translate(0,0); }}
      }}
      @keyframes strike {{
        0%      {{ transform: scale(1.018); }}
        58%,100% {{ transform: scale(1); }}
      }}
      /* No entrance animation on .late/.later. Those elements carry SVG
         transform attributes for placement, and a CSS transform animation
         replaces the attribute outright rather than composing with it —
         which stacks every one of them at the origin. The motion budget goes
         to plate registration, the star ring and the bell crack instead. */
      @keyframes crack {{
        0%, 8%  {{ stroke-dashoffset: 190; }}
        38%     {{ stroke-dashoffset: 0; }}
        92%     {{ stroke-dashoffset: 0; }}
        100%    {{ stroke-dashoffset: 190; }}
      }}
      @keyframes twinkle {{
        0%,100% {{ opacity: .38; transform: scale(.92); }}
        50%     {{ opacity: 1;  transform: scale(1.06); }}
      }}
      @keyframes rule {{ from {{ transform: scaleX(.72) }} to {{ transform: scaleX(1) }} }}

      .plateR {{ animation: registerR 1.5s cubic-bezier(.2,.8,.2,1) both; }}
      .plateB {{ animation: registerB 1.5s cubic-bezier(.2,.8,.2,1) both; }}
      .name   {{ animation: strike 1.5s cubic-bezier(.16,1,.3,1) both;
                 transform-origin: 600px 246px; }}
      .rulein {{ animation: rule 1.1s cubic-bezier(.16,1,.3,1) .25s both; }}
      .crackline {{ stroke-dasharray: 190; animation: crack 6s ease-in-out infinite; }}
      .st {{ transform-box: fill-box; transform-origin: center; }}
"""
    )
    for i in range(13):
        s.append(f"      .s{i} {{ animation: twinkle 3.4s ease-in-out infinite {1.6 + i*0.11:.2f}s; }}\n")
    s.append("    ]]></style>")
    s.append("</defs>")

    s.append(paper_ground("H", W, H, r=4))

    # --- printed border: thick/thin engraved frame -----------------------
    s.append(f'  <rect x="14" y="14" width="{W-28}" height="{H-28}" fill="none" stroke="{INK}" stroke-width="3" opacity="0.88"/>')
    s.append(f'  <rect x="22" y="22" width="{W-44}" height="{H-44}" fill="none" stroke="{INK}" stroke-width="1" opacity="0.6"/>')

    # --- margin ornaments: the bell on the left, the ball on the right ---
    # Kept out of the text block. A watermark behind the name just muddied
    # the type, and the crack read as a stray mark across the standfirst.
    s.append(f"""  <g class="late" opacity="0.62" transform="translate(84 300) scale(0.35)">
    <rect x="-46" y="-206" width="92" height="16" rx="3" fill="{NAVY}"/>
    <ellipse cx="0" cy="-216" rx="11" ry="14" fill="none" stroke="{NAVY}" stroke-width="7"/>
    <rect x="-31" y="-190" width="62" height="14" fill="{NAVY}"/>
    <path d="M-31 -176 C-31 -166 -35 -152 -40 -138
             C-49 -110 -55 -66 -55 -26
             L55 -26 C55 -66 49 -110 40 -138
             C35 -152 31 -166 31 -176 Z" fill="{NAVY}"/>
    <path d="M-66 -26 L66 -26 L66 -8 L-66 -8 Z" fill="{NAVY}"/>
    <ellipse cx="0" cy="-8" rx="66" ry="9" fill="{NAVY}"/>
    <rect x="-5" y="-8" width="10" height="20" rx="2" fill="{NAVY}"/>
    <ellipse cx="0" cy="14" rx="9" ry="11" fill="{NAVY}"/>
    <path class="crackline" d="M20 -14 l14 -30 l-11 -26 l17 -31 l-9 -27 l15 -26"
          fill="none" stroke="{PAPER}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
  </g>""")
    s.append(f"""  <g class="late" opacity="0.62" transform="translate(1116 264)"
       fill="none" stroke="{RED}" stroke-width="3" stroke-linecap="round">
    <circle r="40"/>
    <line x1="-40" y1="0" x2="40" y2="0"/>
    <line x1="0" y1="-40" x2="0" y2="40"/>
    <path d="M-26 -30 C-9 -11 -9 11 -26 30"/>
    <path d="M26 -30 C9 -11 9 11 26 30"/>
  </g>""")

    # --- top line: No. 76 / roundel / MMXXVI -----------------------------
    d, w = P(bask_bold, "No. 76", 20, 1.2)
    s.append(f'  <path class="late" d="{d}" fill="{FADE}" transform="translate(58 70)"/>')
    d, w = P(bask_bold, "MMXXVI", 20, 3.0)
    s.append(f'  <path class="late" d="{d}" fill="{FADE}" transform="translate({W-58-w} 70)"/>')

    # 13 stars in a ring — the Betsy Ross circle, and the Sixers logo
    import math
    star = "M0,-9 L2.4,-3.1 L8.6,-2.8 L3.7,1.2 L5.4,7.2 L0,3.7 L-5.4,7.2 L-3.7,1.2 L-8.6,-2.8 L-2.4,-3.1 Z"
    s.append(f'  <g class="late" transform="translate({cx} 64)">')
    for i in range(13):
        a = -math.pi / 2 + i * (2 * math.pi / 13)
        sx, sy = 42 * math.cos(a), 42 * math.sin(a)
        col = RED if i % 2 == 0 else BLUE
        # Position on the parent <g>, animate on the child. A CSS transform on
        # the path would otherwise replace the placement transform outright and
        # stack all thirteen stars at the centre.
        s.append(f'    <g transform="translate({sx:.2f} {sy:.2f}) scale(.62)">'
                 f'<path class="st s{i}" d="{star}" fill="{col}"/></g>')
    d76, w76 = P(caslon, "76", 44, 1)
    s.append(f'    <path d="{d76}" fill="{INK}" transform="translate({-w76/2:.2f} 15)"/>')
    s.append("  </g>")

    # --- the name, struck in two plates ----------------------------------
    NAME, SIZE, TRACK = "SHAURYA SINGH", 92, 7.0
    dn, wn = P(caslon, NAME, SIZE, TRACK)
    nx = cx - wn / 2
    # Emit the outline once and reference it three times: the file is served
    # on every profile view, so 90KB of duplicated path data is not free.
    s.insert(
        s.index("</defs>"),
        f'<path id="nm" d="{dn}"/>',
    )
    s.append('  <g class="name">')
    # red plate, then blue plate, then the black impression on top:
    # slight misregistration is the whole charm of relief printing
    s.append(f'    <g class="plateR"><use href="#nm" fill="{RED}" opacity="0.9" transform="translate({nx:.2f} 262)"/></g>')
    s.append(f'    <g class="plateB"><use href="#nm" fill="{BLUE}" opacity="0.9" transform="translate({nx:.2f} 262)"/></g>')
    s.append(f'    <use href="#nm" fill="{INK}" transform="translate({nx:.2f} 262)" filter="url(#blotH)"/>')
    s.append("  </g>")

    # --- ornamental rule with a centre lozenge ---------------------------
    s.append(f'  <g class="rulein" style="transform-origin:{cx}px 292px">')
    s.append(f'    <line x1="150" y1="292" x2="{cx-58}" y2="292" stroke="{INK}" stroke-width="2.4"/>')
    s.append(f'    <line x1="{cx+58}" y1="292" x2="{W-150}" y2="292" stroke="{INK}" stroke-width="2.4"/>')
    s.append(f'    <line x1="150" y1="297" x2="{cx-58}" y2="297" stroke="{INK}" stroke-width="0.9" opacity=".6"/>')
    s.append(f'    <line x1="{cx+58}" y1="297" x2="{W-150}" y2="297" stroke="{INK}" stroke-width="0.9" opacity=".6"/>')
    s.append(f'    <path d="M{cx-34} 294 l16 -9 l18 9 l-18 9 z" fill="{RED}"/>')
    s.append(f'    <path d="M{cx+2} 294 l16 -9 l18 9 l-18 9 z" fill="{BLUE}"/>')
    s.append("  </g>")

    # --- the standfirst, colonial broadside voice ------------------------
    line, _ = centered(bask_bold, "BUILDER OF AGENTS  ·  FIXER OF OTHER PEOPLE'S CODE", 21, 2.6, cx, 336, INK, 'class="late"')
    s.append("  " + line)
    line, _ = centered(bask_ital, "One hundred merges into the commons, and counting.", 25, 0, cx, 374, NAVY, 'class="later"')
    s.append("  " + line)

    # --- footer imprint, the way a printer signs a broadside -------------
    line, _ = centered(bask_reg, "PRINTED AT FREMONT, CALIFORNIA  ·  SET IN CASLON  ·  CLASS OF MMXXIX", 13, 2.2, cx, 414, FADE, 'class="later"')
    s.append("  " + line)

    s.append("</svg>")
    return "\n".join(s)


# =========================================================================
# LEDGER — the stat line, as a printer's tally
# =========================================================================
def ledger():
    W, H = 1200, 204
    s = [
        f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="94 merges, 40 organisations, 2 hackathon wins, $225K saved in demo">',
        "<defs>",
        paper_defs("L", W, H),
        f"""<style><![CDATA[
      /* Motion only — never a reveal. See the note in hero(). */
      @keyframes rise {{ from {{ transform: translateY(13px) }} to {{ transform: translateY(0) }} }}
      @keyframes drawUp {{ from {{ transform: scaleY(.4) }} to {{ transform: scaleY(1) }} }}
      .c1 {{ animation: rise .8s cubic-bezier(.16,1,.3,1) .05s both }}
      .c2 {{ animation: rise .8s cubic-bezier(.16,1,.3,1) .17s both }}
      .c3 {{ animation: rise .8s cubic-bezier(.16,1,.3,1) .29s both }}
      .c4 {{ animation: rise .8s cubic-bezier(.16,1,.3,1) .41s both }}
      .div {{ animation: drawUp .7s ease-out .3s both; transform-origin: center }}
    ]]></style>""",
        "</defs>",
        paper_ground("L", W, H, r=4),
        f'  <rect x="10" y="10" width="{W-20}" height="{H-20}" fill="none" stroke="{INK}" stroke-width="2.2" opacity=".85"/>',
        f'  <rect x="17" y="17" width="{W-34}" height="{H-34}" fill="none" stroke="{INK}" stroke-width="0.8" opacity=".5"/>',
    ]

    # Caslon sets figures oldstyle — 4 and 9 descend below the baseline, which
    # is right for a ledger but means the accent rule has to clear them.
    stats = [
        ("100", "MERGES LANDED", RED),
        ("21", "ORGANIZATIONS", BLUE),
        ("44", "REPOSITORIES", RED),
        ("$225K", "SAVED IN DEMO", BLUE),
    ]
    slot = (W - 60) / len(stats)
    for i, (num, lab, col) in enumerate(stats):
        cx = 30 + slot * (i + 0.5)
        dn, wn = P(caslon, num, 62, 0)
        s.append(f'  <g class="c{i+1}">')
        s.append(f'    <path d="{dn}" fill="{INK}" transform="translate({cx-wn/2:.2f} 96)"/>')
        s.append(f'    <line x1="{cx-28}" y1="130" x2="{cx+28}" y2="130" stroke="{col}" stroke-width="1.8"/>')
        dl, wl = P(bask_bold, lab, 13, 3.0)
        s.append(f'    <path d="{dl}" fill="{col}" transform="translate({cx-wl/2:.2f} 152)"/>')
        s.append("  </g>")
        if i < len(stats) - 1:
            dx = 30 + slot * (i + 1)
            s.append(f'  <line class="div" x1="{dx}" y1="46" x2="{dx}" y2="158" stroke="{INK}" stroke-width="0.9" opacity=".35"/>')

    dt, wt = P(bask_bold, "THE LEDGER  ·  AUGUST MMXXVI", 12, 3.4)
    s.append(f'  <path d="{dt}" fill="{FADE}" transform="translate({(W-wt)/2:.2f} 182)"/>')
    s.append("</svg>")
    return "\n".join(s)


# =========================================================================
# SECTION RULES — engraved headers
# =========================================================================
def rule(name, numeral, title, accent):
    W, H = 1200, 86
    uid = "R" + name
    s = [
        f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="{title}">',
        "<defs>",
        paper_defs(uid, W, H),
        f"""<style><![CDATA[
      /* The accent bar may wipe from nothing — it is pure decoration. The
         numeral and title only ever slide, so the header reads at t=0. */
      @keyframes wipe{uid} {{ from {{ transform: scaleX(0) }} to {{ transform: scaleX(1) }} }}
      @keyframes slide{uid} {{ from {{ transform: translateX(-9px) }} to {{ transform: translateX(0) }} }}
      .w{uid} {{ animation: wipe{uid} 1.1s cubic-bezier(.16,1,.3,1) both; transform-origin: 0 0 }}
      .t{uid} {{ /* placement is an SVG attribute; leave it alone */ }}
    ]]></style>""",
        "</defs>",
        paper_ground(uid, W, H, r=3),
        f'  <rect class="w{uid}" x="0" y="0" width="{W}" height="5" fill="{accent}"/>',
        f'  <line x1="0" y1="{H-3}" x2="{W}" y2="{H-3}" stroke="{INK}" stroke-width="2" opacity=".8"/>',
    ]
    # roman numeral in a printed square
    s.append(f'  <g class="t{uid}">')
    s.append(f'    <rect x="30" y="26" width="40" height="40" fill="{INK}"/>')
    dn, wn = P(bask_bold, numeral, 20, 1.0)
    s.append(f'    <path d="{dn}" fill="{PAPER}" transform="translate({50-wn/2:.2f} 54)"/>')
    dt, wt = P(caslon, title, 40, 4.0)
    s.append(f'    <path d="{dt}" fill="{INK}" transform="translate(90 58)"/>')
    # trailing rule out to the right edge
    s.append(f'    <line x1="{90+wt+22}" y1="46" x2="{W-30}" y2="46" stroke="{accent}" stroke-width="1.4" opacity=".55"/>')
    s.append("  </g>")
    s.append("</svg>")
    return "\n".join(s)


SECTIONS = [
    ("career", "I", "Career Highlights", "RED"),
    ("builds", "II", "Featured Builds", "BLUE"),
    ("merges", "III", "The Merge Docket", "RED"),
    ("stack", "IV", "The Stack", "BLUE"),
    ("court", "V", "Off the Court", "RED"),
    ("reach", "VI", "Reach Me", "BLUE"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    total = 0
    for dark in (False, True):
        set_theme(dark)
        suf = "-dark" if dark else ""
        files = {f"hero{suf}.svg": hero(), f"ledger{suf}.svg": ledger()}
        # Accent colours are looked up after set_theme, so SECTIONS stores keys.
        for name, num, title, key in SECTIONS:
            files[f"rule-{name}{suf}.svg"] = rule(name, num, title, globals()[key])
        for fn, body in files.items():
            with open(os.path.join(OUT, fn), "w") as f:
                f.write(body)
            total += len(body)
            print(f"{fn:24} {len(body)/1024:6.1f} KB")
    print(f"{'total':24} {total/1024:6.1f} KB")


if __name__ == "__main__":
    main()
