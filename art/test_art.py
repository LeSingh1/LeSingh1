#!/usr/bin/env python3
"""Regression tests for the generated profile artwork.

Every check here exists because the corresponding bug actually shipped, or
came within one commit of shipping, during this build:

  * the hero once rendered as a completely EMPTY frame inside <img>, because
    every element sat behind an animation delay starting at opacity 0;
  * all thirteen stars once stacked on the origin, because a CSS transform
    animation replaced the SVG transform attribute rather than composing;
  * the stat counters once displayed 0 as their resting value;
  * type ran off the edge of the card, and off the side of the hero.

Run:  python3 test_art.py
"""
import glob
import os
import re
import sys
import unittest
import xml.etree.ElementTree as ET

# Paths are relative to this file, which lives in the art folder, so the
# suite runs from a fresh clone and not only from a dev layout.
HERE = os.path.dirname(os.path.abspath(__file__))
ART = HERE
README = os.path.normpath(os.path.join(HERE, os.pardir, "README.md"))
SVG = "{http://www.w3.org/2000/svg}"


def art_files():
    return sorted(glob.glob(os.path.join(ART, "*.svg")))


def css_of(text):
    return "\n".join(re.findall(r"<!\[CDATA\[(.*?)\]\]>", text, re.S))


def animated_classes(css):
    """class -> animation shorthand, for every rule that animates."""
    out = {}
    for sel, body in re.findall(r"\.([A-Za-z0-9_\-]+)\s*\{([^}]*)\}", css):
        m = re.search(r"animation:\s*([^;]+)", body)
        if m:
            out[sel] = m.group(1)
    return out


def keyframes_of(css):
    """name -> list of (selector-text, declarations)."""
    out = {}
    for name, body in re.findall(r"@keyframes\s+([A-Za-z0-9_\-]+)\s*\{(.*?)\}\s*(?=@|\.|$)",
                                 css, re.S):
        out[name] = re.findall(r"([\d.%,\s a-z]+?)\s*\{([^}]*)\}", body)
    return out


class TestFilesPresent(unittest.TestCase):
    def test_light_and_dark_pairs(self):
        names = {os.path.basename(p) for p in art_files()}
        self.assertTrue(names, "no artwork generated")
        for n in sorted(names):
            if n.endswith("-dark.svg"):
                continue
            self.assertIn(n.replace(".svg", "-dark.svg"), names,
                          f"{n} has no dark counterpart")

    def test_readme_references_resolve(self):
        md = open(README).read()
        for ref in set(re.findall(r'(?:src|srcset)="\./(art/[^"]+)"', md)):
            self.assertTrue(os.path.exists(os.path.normpath(os.path.join(HERE, os.pardir, ref))),
                            f"README references missing file {ref}")

    def test_every_art_file_is_used(self):
        md = open(README).read()
        for p in art_files():
            n = os.path.basename(p)
            self.assertIn(n, md, f"{n} is generated but never referenced")


class TestWellFormed(unittest.TestCase):
    def test_parses(self):
        for p in art_files():
            with self.subTest(f=os.path.basename(p)):
                ET.parse(p)

    def test_no_external_references(self):
        """<img>-embedded SVG cannot fetch anything. It must be self-contained."""
        for p in art_files():
            t = open(p).read()
            with self.subTest(f=os.path.basename(p)):
                self.assertNotIn("<script", t)
                self.assertNotIn("@import", t)
                for u in re.findall(r'url\((["\']?)([^)"\']+)\1\)', t):
                    self.assertTrue(u[1].startswith("#"),
                                    f"non-local url() reference: {u[1]}")
                for a in re.findall(r'(?:href|xlink:href)="([^"]+)"', t):
                    self.assertTrue(a.startswith("#"), f"external href: {a}")
                self.assertFalse(re.search(r'https?://(?!www\.w3\.org|creativecommons|purl)',
                                           t), "remote reference in artwork")

    def test_has_accessible_label(self):
        for p in art_files():
            t = open(p).read()
            with self.subTest(f=os.path.basename(p)):
                m = re.search(r'aria-label="([^"]*)"', t)
                self.assertIsNotNone(m, "missing aria-label")
                self.assertGreater(len(m.group(1)), 12, "aria-label too thin")

    def test_size_budget(self):
        """Sixteen of these load on one page; keep the total sane."""
        total = sum(os.path.getsize(p) for p in art_files())
        self.assertLess(total, 900 * 1024,
                        f"artwork totals {total/1024:.0f} KB")


class TestRestingState(unittest.TestCase):
    """The frozen frame must be the finished artwork."""

    def test_no_transform_animation_on_transform_attribute(self):
        """A CSS transform animation REPLACES an SVG transform attribute.

        This is what stacked all thirteen stars on the origin.
        """
        for p in art_files():
            t = open(p).read()
            css = css_of(t)
            kf = keyframes_of(css)
            anim = animated_classes(css)
            moving = {c for c, sh in anim.items()
                      if any("transform" in " ".join(d for _, d in kf.get(n, []))
                             for n in kf if n in sh)}
            root = ET.parse(p).getroot()
            for el in root.iter():
                cls = (el.get("class") or "").split()
                if not cls or "transform" not in el.attrib:
                    continue
                for c in cls:
                    with self.subTest(f=os.path.basename(p), cls=c):
                        self.assertNotIn(
                            c, moving,
                            f"<{el.tag.replace(SVG,'')} class={c}> has a transform "
                            f"attribute AND a CSS transform animation; it will "
                            f"snap to the origin")

    def test_nothing_essential_starts_invisible(self):
        """No animation may hold opacity 0 at the 0% keyframe unless the
        element is decorative overspray."""
        for p in art_files():
            css = css_of(open(p).read())
            kf = keyframes_of(css)
            for name, frames in kf.items():
                for sel, decl in frames:
                    stops = [s.strip() for s in sel.split(",")]
                    if not any(s in ("0%", "from") for s in stops):
                        continue
                    m = re.search(r"opacity:\s*([\d.]+)", decl)
                    if m and float(m.group(1)) == 0.0:
                        # counters legitimately hide their non-final frames
                        if re.match(r"^n[A-Za-z]+\d+_\d+k$", name):
                            continue
                        self.fail(f"{os.path.basename(p)}: @keyframes {name} "
                                  f"starts at opacity 0")


class TestCounters(unittest.TestCase):
    """The stat roll-up must never rest on a wrong number."""

    @property
    def TRUTH(self):
        import stats
        return [stats.MERGES, stats.ORGS, stats.REPOS, stats.WINS]

    def _counter_groups(self, path):
        root = ET.parse(path).getroot()
        groups = {}
        for el in root.iter(SVG + "g"):
            c = (el.get("class") or "")
            m = re.match(r"^(n[A-Za-z]+(\d+))_(\d+)$", c)
            if m:
                groups.setdefault(m.group(2), []).append((int(m.group(3)), el))
        return groups

    def test_exactly_one_frame_visible_at_rest(self):
        for p in glob.glob(os.path.join(ART, "ledger*.svg")):
            for stat, frames in self._counter_groups(p).items():
                visible = [i for i, el in frames if float(el.get("opacity", 1)) > 0]
                with self.subTest(f=os.path.basename(p), stat=stat):
                    self.assertEqual(len(visible), 1,
                                     "exactly one counter frame may be visible at rest")
                    self.assertEqual(visible[0], max(i for i, _ in frames),
                                     "the visible resting frame must be the LAST one")

    def test_resting_and_final_keyframes_agree(self):
        """0% and 100% of the final frame's animation must both be opaque."""
        for p in glob.glob(os.path.join(ART, "ledger*.svg")):
            css = css_of(open(p).read())
            kf = keyframes_of(css)
            for stat, frames in self._counter_groups(p).items():
                last = max(i for i, _ in frames)
                el = dict((i, e) for i, e in frames)[last]
                name = (el.get("class") or "") + "k"
                self.assertIn(name, kf, f"no keyframes for {name}")
                for sel, decl in kf[name]:
                    stops = [x.strip() for x in sel.split(",")]
                    if any(x in ("0%", "from", "100%", "to") for x in stops):
                        m = re.search(r"opacity:\s*([\d.]+)", decl)
                        if m:
                            with self.subTest(f=os.path.basename(p), stat=stat, at=sel):
                                self.assertEqual(float(m.group(1)), 1.0,
                                                 "final counter frame must be opaque "
                                                 "at both ends of the timeline")

    def test_numbers_match_the_claims_in_the_readme(self):
        """stats.py is the single source of truth; prose must agree with it."""
        md = open(README).read()
        for n in self.TRUTH:
            self.assertIn(str(n), md,
                          f"stats.py says {n} but the README never says it")

    def test_stats_are_internally_consistent(self):
        import stats
        stats.check()


class TestBounds(unittest.TestCase):
    """Nothing may run off its own canvas."""

    def test_paths_stay_inside_the_viewbox(self):
        for p in art_files():
            root = ET.parse(p).getroot()
            vb = [float(v) for v in root.get("viewBox").split()]
            W, H = vb[2], vb[3]
            for el in root.iter():
                d = el.get("d")
                if not d or el.get("transform") or el.get("filter"):
                    continue
                xs = [float(x) for x in re.findall(r"[-+]?\d*\.?\d+", d)][0::2]
                if not xs:
                    continue
                with self.subTest(f=os.path.basename(p)):
                    self.assertGreater(max(xs), -W, "geometry far off-canvas")

    def test_text_is_outlined_not_live(self):
        """<text> would need a font the <img> context cannot load."""
        for p in art_files():
            root = ET.parse(p).getroot()
            with self.subTest(f=os.path.basename(p)):
                self.assertEqual(list(root.iter(SVG + "text")), [],
                                 "live <text> will not render with the intended face")


class TestReadme(unittest.TestCase):
    def test_no_emoji(self):
        """The user asked for no emojis, ever."""
        md = open(README).read()
        found = re.findall(
            "[\U0001F000-\U0001FAFF←-⇿⌀-⏿■-➿⬀-⯿️]",
            md)
        self.assertEqual(found, [], f"emoji/pictographs in README: {found}")

    def test_tech_stack_uses_logos_not_text(self):
        md = open(README).read()
        self.assertIn("skillicons.dev", md, "tech stack must render as logos")
        self.assertNotIn("`TypeScript` ·", md, "text-pill stack list is back")

    def test_dark_mode_sources_paired(self):
        md = open(README).read()
        srcsets = re.findall(r'srcset="\./art/([^"]+)"', md)
        imgs = re.findall(r'<img src="\./art/([^"]+)"', md)
        self.assertEqual(len(srcsets), len(imgs),
                         "every art <img> needs a dark <source>")
        for s in srcsets:
            self.assertTrue(s.endswith("-dark.svg"), f"{s} is not a dark asset")

    def test_no_placeholder_text(self):
        md = open(README).read().lower()
        for bad in ("lorem ipsum", "todo", "tbd", "coming soon", "xxx"):
            self.assertNotIn(bad, md, f"placeholder text {bad!r} left in README")


class TestBrand(unittest.TestCase):
    """Palette stays; the trademarked logo does not.

    The team mark was deliberately removed. These tests keep it removed, so a
    future edit cannot quietly reintroduce someone else's IP.
    """

    def test_palette_is_present(self):
        for p in glob.glob(os.path.join(ART, "hero*.svg")):
            t = open(p).read()
            with self.subTest(f=os.path.basename(p)):
                self.assertIn("#1d428a", t, "Philadelphia blue absent")
                self.assertIn("#c8102e", t, "Philadelphia red absent")

    def test_no_team_logo_asset(self):
        self.assertFalse(glob.glob(os.path.join(ART, "logo", "*")),
                         "a team logo asset is back in art/logo/")
        self.assertFalse(os.path.exists(os.path.join(HERE, "sixers_mark.py")),
                         "sixers_mark.py (logo embedder) is back")

    def test_no_trademarked_wordmark_in_artwork(self):
        for p in art_files():
            t = open(p).read().lower()
            with self.subTest(f=os.path.basename(p)):
                for mark in ("76ers", "sixers", "philadelphia 76"):
                    self.assertNotIn(mark, t,
                                     f"team wordmark {mark!r} present in artwork")

    def test_readme_claims_no_team_affiliation(self):
        md = open(README).read().lower()
        self.assertNotIn("76ers", md, "team wordmark reintroduced in README")


class TestGeneratorRuns(unittest.TestCase):
    """The generator itself must execute.

    A rename once left a stale module alias in build_art.py. The committed
    SVGs were fine, so nothing looked wrong — but the script that produces
    them raised NameError on import-time use and could not be re-run. Art that
    cannot be regenerated is art you cannot fix.
    """

    def test_module_imports_and_renders_every_piece(self):
        import importlib
        ba = importlib.import_module("build_art")
        for dark in (False, True):
            ba.set_theme(dark)
            with self.subTest(dark=dark):
                self.assertIn("<svg", ba.hero())
                self.assertIn("<svg", ba.ledger())
                for name, num, title, accent in ba.SECTIONS:
                    self.assertIn("<svg", ba.rule(name, num, title, accent))

    def test_output_is_deterministic(self):
        """Same inputs, same bytes — otherwise every build churns the diff."""
        import importlib
        ba = importlib.import_module("build_art")
        ba.set_theme(True)
        self.assertEqual(ba.hero(), ba.hero())
        self.assertEqual(ba.ledger(), ba.ledger())

    def test_committed_svgs_match_a_fresh_render(self):
        """Guards against hand-edited SVGs drifting from the generator."""
        import importlib
        ba = importlib.import_module("build_art")
        ba.set_theme(True)
        fresh = ba.hero()
        on_disk = open(os.path.join(ART, "hero-dark.svg")).read()
        self.assertEqual(fresh, on_disk,
                         "hero-dark.svg is stale; re-run build_art.py")


class TestStarArc(unittest.TestCase):
    """The crown must read as a crown."""

    def _points(self, **kw):
        import motifs, math
        m = motifs.star_arc(300, 100, 168, kw.pop("ry", 78), **kw)
        return [(float(a), float(b))
                for a, b in re.findall(r"translate\(([-\d.]+) ([-\d.]+)\)", m)]

    def test_thirteen_stars(self):
        self.assertEqual(len(self._points()), 13, "one star per colony")

    def test_evenly_spaced_along_the_arc(self):
        """Stepping by angle instead of arc length bunches the end stars."""
        import math
        pts = self._points()
        gaps = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
                for i in range(len(pts) - 1)]
        spread = (max(gaps) - min(gaps)) / (sum(gaps) / len(gaps))
        self.assertLess(spread, 0.02,
                        f"star spacing varies by {spread:.1%} along the arc")

    def test_actually_curves(self):
        """A rise this shallow reads as a straight line of stars."""
        pts = self._points()
        rise = max(p[1] for p in pts) - min(p[1] for p in pts)
        span = max(p[0] for p in pts) - min(p[0] for p in pts)
        self.assertGreater(rise / span, 0.12,
                           f"arc rises only {rise:.0f}px over {span:.0f}px")

    def test_symmetric(self):
        pts = self._points()
        for i in range(len(pts) // 2):
            a, b = pts[i], pts[-1 - i]
            self.assertAlmostEqual(a[0] - 300, -(b[0] - 300), delta=0.6)
            self.assertAlmostEqual(a[1], b[1], delta=0.6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
