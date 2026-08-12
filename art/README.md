# Artwork

The profile art is generated, not hand-written. `build_art.py` emits every SVG
in this folder, in a light and a dark inking.

```
python3 build_art.py
```

Two things worth knowing before editing:

**Type is baked to outlines.** GitHub renders README images inside `<img>`,
which cannot load a webfont. `text2path.py` converts strings to vector paths
with fontTools so Caslon survives on machines that have never heard of it.
Requires `fonttools` and macOS system fonts (Big Caslon, Baskerville).

**The resting state is the artwork.** No essential element animates in from
`opacity: 0`. If a renderer never advances the timeline — a link preview card,
a thumbnailer, an `<img>` rasterised at t=0 — the sheet must still read as
finished. Motion is enhancement only.

**Do not put a CSS transform animation on an element that carries an SVG
`transform` attribute.** The CSS transform replaces the attribute rather than
composing with it, and the element jumps to the origin. Animate a child, or
wrap it in a positioned `<g>`.
