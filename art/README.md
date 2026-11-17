# Artwork

Generated, not hand-drawn. `build_art.py` emits every SVG in this folder, in a
light and a dark variant. `test_art.py` enforces the invariants that keep them
from breaking, and checks the profile README too.

```bash
pip3 install fonttools
python3 build_art.py     # regenerate all 18 SVGs
python3 test_art.py      # regression tests
```

## What it draws

A **blueprint drawing sheet**. The dark variant is blueprint navy `#0a1628`
with cyan linework `#7cc4ff` and amber callouts `#ffb547`. The light variant
is drafting-paper white `#f7f9fc` with deep blue linework `#1f4fa0` and
orange-red callouts `#d9480f`.

The hero is an engineering drawing of an original two-finger robot gripper
holding a ball. It has what a real drawing sheet has: a bordered frame with
zone letters and numbers, centring marks, a revision block, notes, a title
block, a front view and a detail view. The dimension callouts carry the real
numbers from `stats.py`. Detail A, at 4:1, shows the planned contact
microphone on the fingertip, which is the research project the README
describes. Every shape is original; there are no logos or borrowed marks.

The section strips use the same language: a numbered title cell, a leader
running into a lettered balloon, and scale ticks along the lower edge.

`blueprint.py` holds the drafting primitives (paths, arrowheads, hatching,
fitted type, the pencil and ink layers). `build_art.py` composes the sheets.

## Where the numbers come from

`stats.py` is the single source of truth for merges, organizations,
repositories and wins. The generator draws the callouts from it, and
`test_art.py` fails if the outlined callout glyphs, the hero's accessible
label, or the README prose disagree with it, or if the per-organization counts
do not add up.

Counted from merged pull requests authored by `LeSingh1`, **excluding this
account's own repositories**. Two Meta contributions landed through
Phabricator, which closes the pull request without marking it merged, so a
plain merged search undercounts by exactly those two.

## Five rules, each learned by breaking it

**1. Type is baked to vector outlines.** GitHub renders README images inside
`<img>`, which cannot load a webfont. `text2path.py` converts strings to paths
with fontTools, using the macOS faces DIN Condensed Bold, DIN Alternate Bold
and Menlo Bold. `test_text_is_outlined_not_live` enforces it.

**2. Never put a CSS transform animation on an element that also carries an
SVG `transform` attribute.** CSS wins outright and *replaces* the attribute
instead of composing with it. An earlier version stacked a row of stars on
the origin this way. This artwork animates only `stroke-dashoffset` and
`opacity`, and `test_only_safe_properties_animate` keeps it that way.

**3. A frozen frame must still read.** Preview cards and thumbnailers
rasterise at `t=0` without running the timeline. An early hero rendered as an
empty frame because everything started at `opacity: 0`. So every line that
draws itself on sits over a faint pencil copy of the same geometry, and type
inks up from a ghost instead of from nothing. Frozen at `t=0`, the sheet is a
complete drawing in pencil. `test_every_draw_on_line_has_a_pencil_underlay`
and `test_nothing_starts_at_zero_opacity` enforce it.

**4. Motion is optional.** Every SVG carries a
`prefers-reduced-motion: reduce` block that stops every animation, which
leaves the finished drawing. Only one thing loops: the caret after the
`$ ./listen --for slip` note. `test_reduced_motion_stops_everything` and
`test_exactly_one_loop` enforce both.

**5. No em dashes or en dashes, anywhere.** Not in the README, the alt text,
the SVG labels, or the source. `test_no_em_or_en_dashes_anywhere` scans every
text file.

## Layout

Nothing is positioned by eye where it can be measured. `fit()` shrinks a
string until it clears the space actually available and `wrap()` breaks the
notes on measured widths, so copy can change without pushing type off an
edge.

## The snake

`.github/workflows/snake.yml` runs `Platane/snk` once a day and publishes a
light and a dark snake, in this palette, to the `output` branch. The README
embeds both as a `<picture>` pair.
