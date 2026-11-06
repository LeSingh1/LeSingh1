#!/usr/bin/env python3
"""The numbers, in one place.

Both the artwork generator and the test suite read these, so the card, the
ledger and the README prose cannot drift apart. Refresh with:

    gh api -X GET search/issues -f q='author:LeSingh1 is:pr is:merged' ...

counting merged PRs authored by LeSingh1, EXCLUDING this account's own
repositories. Two Meta contributions land through Phabricator, which closes
the pull request without marking it merged — a naive search undercounts by
those two. See art/README.md.
"""

MERGES = 132        # merged into external projects
ORGS = 25           # distinct organizations
REPOS = 50          # distinct repositories
WINS = 2            # hackathons won
LEXICAL = 36        # merged into facebook/lexical, shown on the card

AS_OF = "November 2026"

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
