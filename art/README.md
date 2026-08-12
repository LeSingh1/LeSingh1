# Artwork

Generated, not hand-written. `build_art.py` emits every SVG here, in a light
and a dark variant.

```
pip3 install fonttools && python3 build_art.py
```

Visual language: 76ers blue and red, hard diagonal colour blocks, ben-day
halftone, diagonal hatching, a thirteen-star arc, red/white/blue stripe bars,
and heavy condensed type. The `76` roundel is original artwork — it borrows the
palette and the 1776 star motif, it is not a trace of the team's logo.

Three rules, all learned by breaking them:

**Type is baked to outlines.** GitHub renders README images inside `<img>`,
which cannot load a webfont. `text2path.py` converts strings to vector paths
with fontTools. Needs macOS system fonts (Helvetica Neue Condensed Black,
DIN Condensed Bold).

**The resting state must be the finished artwork.** Link-preview cards and
thumbnailers can rasterise an SVG at `t=0` without ever advancing the timeline.
Nothing essential may animate in from `opacity: 0`, and no number may animate
in from a wrong value — the stat counters hold their true figure at both the
0% and 100% keyframe, so the count-up only exists in between. An earlier draft
of this banner rendered as an empty frame for exactly this reason.

**Never put a CSS transform animation on an element that carries an SVG
`transform` attribute.** The CSS transform replaces the attribute instead of
composing with it, and the element snaps to the origin. Animate a child, or
wrap it in a positioned `<g>`.

Text is fitted, never hardcoded: `fit()` shrinks a string until it clears the
space actually available at its own baseline, which for the hero means
accounting for the blue wedge leaning left as it descends.
