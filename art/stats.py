#!/usr/bin/env python3
"""The numbers, in one place.

The drawing generator, the test suite and the README all read or check these,
so the dimension callouts and the prose cannot drift apart. Refresh with:

    gh search prs --author LeSingh1 --merged --limit 1000 \\
        --json repository,number,title,url

then count pull requests whose repository owner is NOT LeSingh1. Two Meta
contributions landed through Phabricator, which closes the pull request
without marking it merged, so a plain merged search undercounts by exactly
those two:

    pyrefly#3415   landed as 92413ec  (repo since moved to pyrefly-org)
    idb#926        landed as 00464e8

Both are counted under Meta, where they landed. See art/README.md.
"""

AS_OF = "November 2026"

# 130 found by the merged search, plus the two Phabricator landings above.
SEARCH_MERGED = 130
PHABRICATOR = 2

MERGES = SEARCH_MERGED + PHABRICATOR   # merged into other people's projects
ORGS = 25                              # distinct organizations
REPOS = 50                             # distinct repositories (48 + pyrefly + idb)
WINS = 4                               # hackathons won
LEXICAL = 36                           # merged into meta/lexical (was facebook/lexical)

# Per-organization merge counts, for the docket table in the README.
BY_ORG = {
    "meta": 42, "apple": 20, "NVIDIA": 20, "openai": 10, "microsoft": 6,
    "google": 5, "fastify": 4, "denoland": 4, "cloudflare": 4, "jestjs": 2,
}
SINGLES = 15        # organizations with exactly one merge


def check():
    """The parts must add up to the whole."""
    assert sum(BY_ORG.values()) + SINGLES == MERGES, (
        f"{sum(BY_ORG.values())} + {SINGLES} != {MERGES}")
    assert len(BY_ORG) + SINGLES == ORGS, (
        f"{len(BY_ORG)} + {SINGLES} != {ORGS}")


check()
