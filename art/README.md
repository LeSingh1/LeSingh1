# Artwork

Generated, not hand-drawn. `build_art.py` emits every SVG in this folder, in a
light and a dark variant. `test_art.py` enforces the invariants that keep them
from breaking.

```bash
pip3 install fonttools
python3 build_art.py     # regenerate all 16 SVGs
python3 test_art.py      # 23 regression tests
```

## What it draws

A **graffiti rookie card**: a foil-edged trading card centred on a
spray-painted wall — splatter, drips, overspray, halftone, ghosted
basketballs and thrown tags.

The centrepiece is the headline number, set the way a jersey number is set —
white over an offset red and blue impression. A real card puts a photograph
there; the honest substitute is the one figure on the card that is actually
his.

Two earlier revisions put borrowed iconography in that slot: first the real
Philadelphia 76ers mark, then an original jersey. Both were removed. The
palette still carries the theme — Philadelphia blue `#1d428a` and red
`#c8102e` — while every shape in the artwork is original and free of anyone's
trademark. `TestBrand` keeps it that way: it fails if a logo asset, the
`sixers_mark` embedder, or the team wordmark reappears.

The only ornament left from those passes is the thirteen-star arc in
`motifs.py`, which is the 1776 colonies device and belongs to nobody.

## Where the numbers come from

`stats.py` is the single source of truth for merges, organizations and
repositories. The generator reads it, and `test_art.py` fails if the README
prose disagrees with it or if the per-organization counts do not sum to the
total.

Counted from merged pull requests authored by `LeSingh1`, **excluding this
account's own repositories**. Two Meta contributions landed through
Phabricator, which closes the pull request without marking it merged, so a
naive `is:merged` search undercounts by those two.

## Four rules, each learned by breaking it

**1. Type is baked to vector outlines.** GitHub renders README images inside
`<img>`, which cannot load a webfont. `text2path.py` converts strings to paths
with fontTools. Needs the macOS faces Helvetica Neue Condensed Black and DIN
Condensed Bold. `test_text_is_outlined_not_live` enforces it.

**2. Never put a CSS transform animation on an element that also carries an
SVG `transform` attribute.** CSS wins outright and *replaces* the attribute
instead of composing with it. This stacked all thirteen stars of an earlier
mark on the origin, and later silently dropped the `skewX(-20)` from the
holographic sweep, so the "light" was rendering as an upright bar. Animate a
child, or wrap the element in a positioned `<g>`.
`test_no_transform_animation_on_transform_attribute` enforces it.

**3. The resting state must be the finished artwork.** Preview cards and
thumbnailers rasterise at `t=0`, or a few hundred milliseconds in, without
running the timeline to completion. An early hero rendered as a completely
**empty frame** because every element sat behind a delay starting at
`opacity: 0`. `test_nothing_essential_starts_invisible` enforces it.

**4. A counter may never rest on a wrong number.** The stat roll-up holds the
true figure at both the 0% and 100% keyframe, so a frozen render shows the
truth; the count-up only exists in between. Intermediate frames are ghosted at
38% opacity, so a frame caught mid-roll reads as a spinning counter rather
than as data. `TestCounters` enforces both halves.

## Layout

Nothing is positioned by eye. `fit()` shrinks a string until it clears the
space actually available; the card sizes the jersey against the panel it
actually has, including the overhang of the star arc above its shoulders.
Copy can change without pushing type off an edge.
