# Artwork

Generated, not hand-drawn. `build_art.py` emits every SVG in this folder, in a
light and a dark variant, and `test_art.py` checks the invariants that keep
them from breaking.

```bash
pip3 install fonttools
python3 build_art.py     # regenerate all 16 SVGs
python3 test_art.py      # 20 regression tests
```

## What it draws

A Philadelphia 76ers **graffiti rookie card**: a foil-edged trading card
centred on a spray-painted wall — splatter, drips, overspray, halftone,
ghosted basketballs and thrown tags.

`logo/Philadelphia_76ers_logo.svg` is the **real** primary mark (Wikimedia
Commons), inlined by `sixers_mark.py` rather than approximated. Earlier drafts
redrew the swooping 7 by hand and it was never close enough to pass. The team
palette is read off that file, so the artwork and the logo can never drift:
blue `#1d428a`, red `#c8102e`.

> The 76ers name and logo are trademarks of the Philadelphia 76ers / NBA.
> This is fan use on a personal profile page.

## Four rules, each learned by breaking it

**1. Type is baked to vector outlines.** GitHub renders README images inside
`<img>`, which cannot load a webfont. `text2path.py` converts strings to paths
with fontTools. Needs the macOS faces Helvetica Neue Condensed Black and DIN
Condensed Bold. `test_art.py::test_text_is_outlined_not_live` enforces it.

**2. Never put a CSS transform animation on an element that also carries an
SVG `transform` attribute.** CSS wins outright and *replaces* the attribute
instead of composing with it. This stacked all thirteen stars of an earlier
mark on the origin, and later silently dropped the `skewX(-20)` from the
holographic sweep so the "light" was an upright bar. Animate a child, or wrap
the element in a positioned `<g>`.
`test_no_transform_animation_on_transform_attribute` enforces it.

**3. The resting state must be the finished artwork.** Preview cards and
thumbnailers rasterise at `t=0`, or a few hundred milliseconds in, without
running the timeline to completion. An early hero rendered as a completely
**empty frame** because every element sat behind a delay starting at
`opacity: 0`. Nothing essential may animate in from nothing.
`test_nothing_essential_starts_invisible` enforces it.

**4. A counter may never rest on a wrong number.** The stat roll-up holds the
true figure at both the 0% and 100% keyframe, so a frozen render shows the
truth; the count-up only exists in between. Intermediate frames are ghosted at
38% opacity, so a frame caught mid-roll reads as a spinning counter rather
than as data. `TestCounters` enforces both halves.

## Layout

Text is fitted, never hardcoded: `fit()` shrinks a string until it clears the
space actually available, and the card sizes the badge against the panel it
actually has. Copy can change without pushing type off an edge.

## Where the numbers come from

Merges, organizations and repositories are counted from the GitHub API over
merged PRs authored by `LeSingh1`, excluding this account's own repositories.
Two Meta contributions landed through Phabricator, which closes the PR without
marking it merged, so a naive search undercounts. Update the figures in
`build_art.py` (`ledger()`) and in the README together — `test_art.py` checks
that every number in the art also appears in the README.
