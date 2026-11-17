# Artwork

Generated, not hand-drawn. `build_art.py` emits every SVG in this folder, in a
light and a dark variant. `test_art.py` enforces the invariants that keep them
from breaking, and checks the profile README too.

```bash
pip3 install fonttools
python3 build_art.py     # regenerate all 20 SVGs
python3 test_art.py      # regression tests
```

## What it draws

A **1st Edition holo trading card** on a spray-painted wall: splatter, drips,
overspray, halftone, ghosted basketballs and thrown tags. Philadelphia blue
`#1d428a` and red `#c8102e`, with white and silver foil.

`card.py` lays the card out like a collectible battle card. It has a stage
pill and name bar, HP and a type symbol, a foil art window, an info strip
with a 1st Edition stamp, one ability and two moves with damage numbers,
weakness, resistance and retreat, flavor text, then the illustrator line, set
number and rarity star. The frame is a beveled silver border; a holo band
sweeps across the whole card and a foil sheen drifts across the art window.

Everything printed on it is true. HP is the merge count. **Parity Audit**
carries the merges, repositories and organizations. **Fast Break Build** is
the four 2026 hackathon wins. **Digital Twin** is the 375-part robot model
tested in simulation. The set number is the FTC team number, 23543. The
playful lines (weakness, resistance) are jokes, not claims.

The art window shows a ball dropping through a net under the thirteen-star
arc from `motifs.py`, which is the 1776 colonies device and belongs to
nobody. Every shape is original. `TestBrand` fails if a logo asset, the
`sixers_mark` embedder, or a team wordmark reappears.

## Where the numbers come from

`stats.py` is the single source of truth for merges, organizations,
repositories and wins. The generator reads it, and `test_art.py` fails if the
README prose, the ledger counters, the card's HP glyphs or its move text
disagree with it, or if the per-organization counts do not add up.

Counted from merged pull requests authored by `LeSingh1`, **excluding this
account's own repositories**. Two Meta contributions landed through
Phabricator, which closes the pull request without marking it merged, so a
plain merged search undercounts by exactly those two.

## Six rules, each learned by breaking it

**1. Type is baked to vector outlines.** GitHub renders README images inside
`<img>`, which cannot load a webfont. `text2path.py` converts strings to paths
with fontTools. Needs the macOS faces Helvetica Neue Condensed Black, DIN
Condensed Bold and Gill Sans. `test_text_is_outlined_not_live` enforces it.

**2. Never put a CSS transform animation on an element that also carries an
SVG `transform` attribute.** CSS wins outright and *replaces* the attribute
instead of composing with it. This stacked all thirteen stars of an earlier
mark on the origin, and later silently dropped the `skewX(-20)` from the
holographic sweep. Animate a child, or wrap the element in a bare `<g>`.
`test_no_transform_animation_on_transform_attribute` and
`test_moving_parts_are_bare_wrappers` enforce it.

**3. The resting state must be the finished artwork.** Preview cards and
thumbnailers rasterise at `t=0` without running the timeline. An early hero
rendered as a completely **empty frame** because every element sat behind a
delay starting at `opacity: 0`. `test_nothing_essential_starts_invisible`
enforces it.

**4. A counter may never rest on a wrong number.** The ledger roll-up holds
the true figure at both the 0% and 100% keyframe, so a frozen render shows the
truth; the count-up only exists in between. `TestCounters` enforces both
halves.

**5. Motion is optional.** Every SVG carries a
`prefers-reduced-motion: reduce` block that stops all animation, and all
motion is CSS, because SMIL ignores that preference. `TestMotionIsOptional`
enforces both.

**6. No em dashes or en dashes, anywhere.** Not in the README, the alt text,
the SVG labels, or the source. `test_no_em_or_en_dashes_anywhere` scans every
text file.

## Layout

Nothing is positioned by eye. `fit()` shrinks a string until it clears the
space actually available, and the card wraps its move text on measured widths
and raises an error if the copy would overflow the face. Copy can change
without pushing type off an edge.

## The snake

`.github/workflows/snake.yml` runs `Platane/snk` once a day and publishes a
light and a dark snake, in Philadelphia blue and red, to the `output` branch.
The README embeds both as a `<picture>` pair.
