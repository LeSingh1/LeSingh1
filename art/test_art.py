#!/usr/bin/env python3
"""Regression tests for the generated profile artwork and the README.

Most checks exist because the matching bug actually shipped, or came within
one commit of shipping, during an earlier version of this page:

  * a hero once rendered as an EMPTY frame inside <img>, because every element
    sat behind an animation delay starting at opacity 0;
  * stars once stacked on the origin, because a CSS transform animation
    replaced the SVG transform attribute instead of composing with it;
  * the README once quoted numbers the artwork did not show;
  * live <text> once rendered in a fallback font, because <img> cannot load one.

The rest guard the content: no em or en dashes, no retired projects, and
no claims that are not true.

Run:  python3 test_art.py
"""
import glob
import os
import re
import unittest
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ART = HERE
ROOT = os.path.normpath(os.path.join(HERE, os.pardir))
README = os.path.join(ROOT, "README.md")
WORKFLOW = os.path.join(ROOT, ".github", "workflows", "snake.yml")
SVG = "{http://www.w3.org/2000/svg}"


def art_files():
    return sorted(glob.glob(os.path.join(ART, "*.svg")))


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def css_of(text):
    return "\n".join(re.findall(r"<!\[CDATA\[(.*?)\]\]>", text, re.S))


def strip_media(css):
    """Drop @media blocks (the reduced-motion override) from a stylesheet."""
    out, i = [], 0
    for m in re.finditer(r"@media[^{]*\{", css):
        if m.start() < i:
            continue
        out.append(css[i:m.start()])
        depth, j = 1, m.end()
        while depth and j < len(css):
            depth += {"{": 1, "}": -1}.get(css[j], 0)
            j += 1
        i = j
    out.append(css[i:])
    return "".join(out)


def animated_classes(css):
    """class -> animation shorthand, for every rule that animates."""
    css = strip_media(css)
    out = {}
    for sel, body in re.findall(r"\.([A-Za-z0-9_\-]+)\s*\{([^}]*)\}", css):
        m = re.search(r"animation:\s*([^;]+)", body)
        if m:
            out[sel] = m.group(1).strip()
    return out


def keyframes_of(css):
    """name -> list of (selector-text, declarations)."""
    out = {}
    for m in re.finditer(r"@keyframes\s+([A-Za-z0-9_\-]+)\s*\{", css):
        depth, i = 1, m.end()
        while depth and i < len(css):
            depth += {"{": 1, "}": -1}.get(css[i], 0)
            i += 1
        body = css[m.end():i - 1]
        out[m.group(1)] = re.findall(r"([\d.%,\sa-z]+?)\s*\{([^}]*)\}", body)
    return out


def text_files():
    """Every text file a visitor or a reviewer reads."""
    pats = ["README.md", "art/*.md", "art/*.py", "art/*.svg",
            ".github/workflows/*.yml"]
    out = []
    for p in pats:
        out += glob.glob(os.path.join(ROOT, p))
    return sorted(out)


# ------------------------------------------------------------------ files
class TestFilesPresent(unittest.TestCase):
    EXPECTED = ["hero"] + [f"rule-{n}" for n in (
        "highlights", "builds", "opensource", "robotics", "life", "stack",
        "activity", "contact")]

    def test_expected_set(self):
        names = {os.path.basename(p) for p in art_files()}
        want = {f"{b}{s}.svg" for b in self.EXPECTED for s in ("", "-dark")}
        self.assertEqual(names, want)

    def test_light_and_dark_pairs(self):
        names = {os.path.basename(p) for p in art_files()}
        for n in sorted(names):
            if not n.endswith("-dark.svg"):
                self.assertIn(n.replace(".svg", "-dark.svg"), names,
                              f"{n} has no dark counterpart")

    def test_readme_references_resolve(self):
        md = read(README)
        for ref in set(re.findall(r'(?:src|srcset)="\./([^"]+)"', md)):
            self.assertTrue(os.path.exists(os.path.join(ROOT, ref)),
                            f"README references missing file {ref}")

    def test_every_art_file_is_used(self):
        md = read(README)
        for p in art_files():
            n = os.path.basename(p)
            self.assertIn(f"./art/{n}", md, f"{n} is generated but never used")


class TestWellFormed(unittest.TestCase):
    def test_parses(self):
        for p in art_files():
            with self.subTest(f=os.path.basename(p)):
                ET.parse(p)

    def test_no_external_references(self):
        """<img>-embedded SVG cannot fetch anything. It must be self-contained."""
        for p in art_files():
            t = read(p)
            with self.subTest(f=os.path.basename(p)):
                self.assertNotIn("<script", t)
                self.assertNotIn("@import", t)
                for u in re.findall(r'url\((["\']?)([^)"\']+)\1\)', t):
                    self.assertTrue(u[1].startswith("#"),
                                    f"non-local url() reference: {u[1]}")
                for a in re.findall(r'(?:href|xlink:href)="([^"]+)"', t):
                    self.assertTrue(a.startswith("#"), f"external href: {a}")
                self.assertFalse(re.search(r"https?://(?!www\.w3\.org)", t),
                                 "remote reference in artwork")

    def test_has_accessible_label_and_title(self):
        for p in art_files():
            t = read(p)
            with self.subTest(f=os.path.basename(p)):
                m = re.search(r'aria-label="([^"]*)"', t)
                self.assertIsNotNone(m, "missing aria-label")
                self.assertGreater(len(m.group(1)), 12, "aria-label too thin")
                self.assertIn("<title>", t)

    def test_size_budget(self):
        total = sum(os.path.getsize(p) for p in art_files())
        self.assertLess(total, 700 * 1024, f"artwork totals {total / 1024:.0f} KB")


# ------------------------------------------------------------------ motion
class TestMotion(unittest.TestCase):
    """The frozen frame must still read, and motion must be optional."""

    def test_no_transform_animation_on_transform_attribute(self):
        """A CSS transform animation REPLACES an SVG transform attribute.

        This is what once stacked a row of stars on the origin.
        """
        for p in art_files():
            t = read(p)
            css = css_of(t)
            kf = keyframes_of(css)
            anim = animated_classes(css)
            moving = {c for c, sh in anim.items()
                      if any("transform" in " ".join(d for _, d in kf.get(n, []))
                             for n in kf if n in sh)}
            for el in ET.parse(p).getroot().iter():
                cls = (el.get("class") or "").split()
                if "transform" not in el.attrib:
                    continue
                for c in cls:
                    with self.subTest(f=os.path.basename(p), cls=c):
                        self.assertNotIn(c, moving)

    def test_only_safe_properties_animate(self):
        """The drawing animates dashoffset and opacity only."""
        for p in art_files():
            for name, frames in keyframes_of(css_of(read(p))).items():
                for _, decl in frames:
                    props = {d.split(":")[0].strip()
                             for d in decl.split(";") if ":" in d}
                    with self.subTest(f=os.path.basename(p), kf=name):
                        self.assertTrue(props <= {"opacity", "stroke-dashoffset"},
                                        f"unexpected animated properties {props}")

    def test_nothing_starts_at_zero_opacity(self):
        for p in art_files():
            for name, frames in keyframes_of(css_of(read(p))).items():
                for sel, decl in frames:
                    stops = [s.strip() for s in sel.split(",")]
                    if not any(s in ("0%", "from") for s in stops):
                        continue
                    m = re.search(r"opacity:\s*([\d.]+)", decl)
                    if m:
                        with self.subTest(f=os.path.basename(p), kf=name):
                            self.assertGreaterEqual(float(m.group(1)), 0.15,
                                                    "starts invisible")

    def test_every_draw_on_line_has_a_pencil_underlay(self):
        """A line that draws itself on is invisible at t=0, so the same
        geometry must already be on the sheet in pencil."""
        for p in art_files():
            root = ET.parse(p).getroot()
            pencil = "".join(el.get("d") for el in root.iter(SVG + "path")
                             if el.get("class") == "pencil")
            drawn = [el for el in root.iter(SVG + "path")
                     if re.match(r"dr", el.get("class") or "")]
            with self.subTest(f=os.path.basename(p)):
                self.assertTrue(drawn, "no draw-on linework")
                for el in drawn:
                    self.assertEqual(el.get("pathLength"), "1")
                    self.assertIn(el.get("d"), pencil,
                                  "draw-on line with no pencil underlay")

    def test_reduced_motion_stops_everything(self):
        for p in art_files():
            css = css_of(read(p))
            m = re.search(r"@media\s*\(prefers-reduced-motion:\s*reduce\)\s*\{(.*)\}",
                          css, re.S)
            with self.subTest(f=os.path.basename(p)):
                self.assertIsNotNone(m, "no prefers-reduced-motion block")
                self.assertIn("animation: none", m.group(1))
                for cls in animated_classes(css):
                    self.assertIn("." + cls, m.group(1),
                                  f".{cls} still moves under reduced motion")

    def test_exactly_one_loop(self):
        """One subtle looping detail on the hero, and nothing else loops."""
        for p in art_files():
            loops = [c for c, sh in animated_classes(css_of(read(p))).items()
                     if "infinite" in sh]
            want = 1 if os.path.basename(p).startswith("hero") else 0
            with self.subTest(f=os.path.basename(p)):
                self.assertEqual(len(loops), want, f"looping classes: {loops}")


# ------------------------------------------------------------------ numbers
class TestStats(unittest.TestCase):
    def setUp(self):
        import stats
        self.st = stats

    def test_stats_are_internally_consistent(self):
        self.st.check()
        self.assertEqual(self.st.MERGES,
                         self.st.SEARCH_MERGED + self.st.PHABRICATOR)

    def test_hero_label_carries_every_number(self):
        for p in glob.glob(os.path.join(ART, "hero*.svg")):
            label = re.search(r'aria-label="([^"]*)"', read(p)).group(1)
            for v in (self.st.MERGES, self.st.ORGS, self.st.REPOS, self.st.WINS):
                with self.subTest(f=os.path.basename(p), v=v):
                    self.assertIn(str(v), label)

    def test_hero_callouts_are_drawn_from_stats(self):
        """The outlined callout glyphs must be exactly the stats.py figures."""
        import blueprint as B
        want = [B.text_path(B.DIN_ALT, f"Ø{self.st.MERGES}", 52)[0],
                B.text_path(B.DIN_ALT, str(self.st.ORGS), 34)[0],
                B.text_path(B.DIN_ALT, str(self.st.REPOS), 36)[0],
                B.text_path(B.DIN_ALT, str(self.st.WINS), 36)[0]]
        for p in glob.glob(os.path.join(ART, "hero*.svg")):
            t = read(p)
            for d in want:
                with self.subTest(f=os.path.basename(p)):
                    self.assertIn(f'd="{d}"', t)

    def test_readme_prose_agrees(self):
        md = read(README)
        st = self.st
        self.assertIn(f"{st.MERGES} merged pull requests", md)
        self.assertIn(f"{st.REPOS} repositories", md)
        self.assertIn(f"{st.ORGS} organizations", md)
        self.assertIn(f"{st.WINS} hackathon wins", md)
        self.assertIn(f"One of {st.LEXICAL} merges into Lexical", md)

    def test_readme_docket_adds_up(self):
        md = read(README)
        rows = re.findall(r"^\| \*\*([^*]+)\*\* \| [^|]+ \| (\d+) \|$", md, re.M)
        counts = [int(c) for _, c in rows]
        self.assertEqual(sum(counts), self.st.MERGES, "docket rows do not sum")
        self.assertEqual(sorted(counts[:-1], reverse=True),
                         sorted(self.st.BY_ORG.values(), reverse=True))
        self.assertEqual(counts[-1], self.st.SINGLES)


# ------------------------------------------------------------------ type
class TestType(unittest.TestCase):
    def test_text_is_outlined_not_live(self):
        """<text> would need a font the <img> context cannot load."""
        for p in art_files():
            with self.subTest(f=os.path.basename(p)):
                self.assertEqual(list(ET.parse(p).getroot().iter(SVG + "text")),
                                 [])

    def test_paths_stay_near_the_viewbox(self):
        for p in art_files():
            root = ET.parse(p).getroot()
            W, H = [float(v) for v in root.get("viewBox").split()[2:]]
            for el in root.iter(SVG + "path"):
                d = el.get("d")
                if not d or el.get("transform"):
                    continue
                nums = [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", d)]
                with self.subTest(f=os.path.basename(p)):
                    self.assertGreaterEqual(min(nums), -1, "geometry off-canvas")
                    self.assertLessEqual(max(nums), max(W, H) + 1,
                                         "geometry off-canvas")

    def test_palette(self):
        want = {"hero.svg": ("#f7f9fc", "#1f4fa0", "#d9480f"),
                "hero-dark.svg": ("#0a1628", "#7cc4ff", "#ffb547")}
        for fn, cols in want.items():
            t = read(os.path.join(ART, fn))
            for c in cols:
                with self.subTest(f=fn, c=c):
                    self.assertIn(c, t)


# ------------------------------------------------------------------ content
# Built from code points so this file does not contain the characters it bans.
_DASH_CHARS = "".join(chr(c) for c in (0x2012, 0x2013, 0x2014, 0x2015, 0x2212))
DASHES = re.compile("[" + _DASH_CHARS + "]|&(?:mdash|ndash|minus);"
                    "|&#(?:8211|8212|8722|x2013|x2014|x2212);", re.I)


class TestContent(unittest.TestCase):
    def test_no_em_or_en_dashes_anywhere(self):
        for p in text_files():
            hits = DASHES.findall(read(p))
            with self.subTest(f=os.path.relpath(p, ROOT)):
                self.assertEqual(hits, [], "em/en dash or minus sign found")

    def test_no_emoji(self):
        md = read(README)
        found = re.findall("[\U0001F000-\U0001FAFF←-⇿⌀-⏿"
                           "■-➿⬀-⯿️]", md)
        self.assertEqual(found, [], f"emoji or pictographs in README: {found}")

    def test_no_retired_projects_or_topics(self):
        banned = [r"edgeboard", r"edge-models", r"LeSingh1/edge-", r"prizepicks",
                  r"\bbetting\b", r"\bodds\b", r"\bsportsbook", r"espn-api",
                  r"break-the-rules", r"dynasty-gm"]
        for p in [README] + art_files():
            t = read(p)
            for b in banned:
                with self.subTest(f=os.path.basename(p), banned=b):
                    self.assertIsNone(re.search(b, t, re.I))

    def test_no_untrue_claims(self):
        md = read(README).lower()
        for bad in ("eagle", "team captain", "varsity captain",
                    "regional finalist", "roughly a third",
                    "downloads a week", "weekly downloads", "1.98"):
            with self.subTest(bad=bad):
                self.assertNotIn(bad, md)
        self.assertIn("captain of the freshman team in 2025-26", md)
        self.assertIn("only sophomore", md)
        self.assertIn("life scout", md)
        self.assertIn("qualifier finalist", md)
        self.assertIn("qualified for the aime through the amc 10", md)

    def test_research_is_described_as_a_plan(self):
        md = read(README).lower()
        para = md[md.index("next: a sense of touch"):]
        para = para[:para.index("\n\n")]
        self.assertIn("planning", para)
        for word in ("we found", "results show", "detected slip", "accuracy of"):
            self.assertNotIn(word, para)

    def test_no_placeholder_text(self):
        md = read(README).lower()
        for bad in ("lorem ipsum", "todo", "tbd", "coming soon", "xxx"):
            self.assertNotIn(bad, md)

    def test_footer_and_contacts_kept(self):
        md = read(README)
        self.assertIn("Fremont, California · Class of 2029", md)
        for url in ("linkedin.com/in/shaurya-singh-b7591540b",
                    "mailto:sshaurya914@gmail.com",
                    "github.com/LeSingh1?tab=repositories"):
            self.assertIn(url, md)

    def test_tech_stack_uses_logos(self):
        self.assertIn("skillicons.dev", read(README))


class TestPictures(unittest.TestCase):
    def test_every_picture_has_a_dark_source_and_a_light_img(self):
        md = read(README)
        pics = re.findall(r"<picture>(.*?)</picture>", md, re.S)
        self.assertGreaterEqual(len(pics), 12)
        for pic in pics:
            with self.subTest(pic=pic[:80]):
                src = re.search(r'media="\(prefers-color-scheme: dark\)" '
                                r'srcset="([^"]+)"', pic)
                img = re.search(r'<img src="([^"]+)"', pic)
                self.assertIsNotNone(src, "no dark <source>")
                self.assertIsNotNone(img, "no light <img>")
                self.assertNotEqual(src.group(1), img.group(1))
                if src.group(1).startswith("./art/"):
                    self.assertEqual(src.group(1),
                                     img.group(1).replace(".svg", "-dark.svg"))
                self.assertRegex(pic, r'alt="[^"]{8,}"')


    def test_srcset_urls_have_no_commas(self):
        """GitHub splits srcset on commas, so a URL with a raw comma is cut
        short. This once collapsed a row of eight tech icons to one."""
        for url in re.findall(r'srcset="([^"]+)"', read(README)):
            with self.subTest(url=url):
                self.assertNotIn(",", url)


class TestSnakeWorkflow(unittest.TestCase):
    def setUp(self):
        self.y = read(WORKFLOW)

    def test_actions_are_pinned_to_exact_versions(self):
        uses = re.findall(r"uses:\s*(\S+)", self.y)
        self.assertTrue(any(u.startswith("Platane/snk/") for u in uses))
        for u in uses:
            with self.subTest(uses=u):
                self.assertRegex(u, r"@v\d+\.\d+\.\d+$")

    def test_triggers_and_permissions(self):
        self.assertIn("schedule:", self.y)
        self.assertIn("workflow_dispatch:", self.y)
        self.assertRegex(self.y, r"permissions:\s*\n\s*contents: write")
        self.assertIn("target_branch: output", self.y)

    def test_palette_matches_the_theme(self):
        self.assertIn("color_snake=#d9480f", self.y)
        self.assertIn("color_snake=#ffb547", self.y)
        self.assertIn("#1f4fa0", self.y)
        self.assertIn("#7cc4ff", self.y)

    def test_readme_embeds_both_outputs(self):
        md = read(README)
        for f in ("snake.svg", "snake-dark.svg"):
            self.assertIn(f"raw.githubusercontent.com/LeSingh1/LeSingh1/output/{f}",
                          md)
            self.assertIn(f"dist/{f}", self.y)


# ------------------------------------------------------------------ generator
class TestGenerator(unittest.TestCase):
    """Art that cannot be regenerated is art you cannot fix."""

    def test_renders_every_piece(self):
        import importlib
        ba = importlib.import_module("build_art")
        for dark in (False, True):
            ba.set_theme(dark)
            with self.subTest(dark=dark):
                self.assertIn("<svg", ba.hero())
                for name, num, title in ba.SECTIONS:
                    self.assertIn("<svg", ba.rule(name, num, title))

    def test_output_is_deterministic(self):
        import importlib
        ba = importlib.import_module("build_art")
        ba.set_theme(True)
        self.assertEqual(ba.hero(), ba.hero())

    def test_committed_svgs_match_a_fresh_render(self):
        """Guards against hand-edited SVGs drifting from the generator."""
        import importlib
        ba = importlib.import_module("build_art")
        for dark in (False, True):
            ba.set_theme(dark)
            suf = "-dark" if dark else ""
            fresh = {f"hero{suf}.svg": ba.hero()}
            for name, num, title in ba.SECTIONS:
                fresh[f"rule-{name}{suf}.svg"] = ba.rule(name, num, title)
            for fn, body in fresh.items():
                with self.subTest(f=fn):
                    self.assertEqual(body, read(os.path.join(ART, fn)),
                                     f"{fn} is stale; re-run build_art.py")

    def test_no_logo_assets(self):
        """Every shape is original. No borrowed marks, ever."""
        self.assertFalse(glob.glob(os.path.join(ART, "logo", "*")))
        for p in art_files():
            t = read(p).lower()
            for mark in ("76ers", "sixers", "<image"):
                with self.subTest(f=os.path.basename(p), mark=mark):
                    self.assertNotIn(mark, t)


if __name__ == "__main__":
    unittest.main(verbosity=2)
