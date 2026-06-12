<div align="center">

<img src="./rookie-card-v12.svg" alt="Shaurya Singh — Rookie Card, 1st Edition Holo, Lakers" width="100%"/>

</div>

<br/>

<div align="center">

<img src="./stats-banner.svg" alt="37 PRs merged · 11 orgs · $1,100 across two hackathon wins · $225K saved in demo · 50+ PRs in review" width="100%"/>

</div>

<br/>

<!-- ============ CAREER HIGHLIGHTS ============ -->

<img src="./header-career.svg" alt="CAREER HIGHLIGHTS" width="100%"/>

<table>
<tr>
<td width="50%" valign="top">

#### Beta Fund × EverMind Hackathon
First place, Audience Favorite. $600. Built [SwarmMarket](https://github.com/LeSingh1/swarm-market) — an app store for agent experience, where agents publish and install skill-packs over MCP.

#### Beta Fund AI Super Hackathon
First place. $500. Built [ShadowBuyer](https://github.com/LeSingh1/shadowbuyer). Saved a roleplayed Fortune 500 buyer $225K in a single negotiation.

</td>
<td width="50%" valign="top">

#### Flagship merge: meta/pyrefly
[#3415](https://github.com/facebook/pyrefly/pull/3415) landed on `main` via Phabricator. Meta's Python type checker.

#### Reach
37 merges across Meta, Apple, Microsoft, NVIDIA, Google, Cloudflare, OpenAI, Vue, Deno, Jest, Hono, ml-explore. Walked in cold.

</td>
</tr>
</table>

<br/>

<!-- ============ FEATURED BUILDS ============ -->

<img src="./header-builds.svg" alt="FEATURED BUILDS" width="100%"/>

<table>
<tr>
<td width="50%" valign="top">

#### EdgeBoard
A real-time PrizePicks board and lineup optimizer. It pulls the live board, projects each player's stat from their recent game log, calibrates the probability, and scores slips on the real payout tiers. 13 sports, models retrain themselves every day. Next.js and TypeScript. [Repo](https://github.com/LeSingh1/edgeboard).

</td>
<td width="50%" valign="top">

#### edge-models
Player prop projection models for 13 sports, trained on about 147M synthesized rows from real game logs. Isotonic calibration with a clamp that stops it overclaiming, plus an honest per-sport backtest for each one. [Repo](https://github.com/LeSingh1/edge-models).

</td>
</tr>
</table>

<br/>

<!-- ============ FLAGSHIP MERGES ============ -->

<img src="./header-flagship.svg" alt="FLAGSHIP MERGES" width="100%"/>

| Org | PR | What it fixes |
|:---:|---|---|
| **Meta** | [pyrefly#3415](https://github.com/facebook/pyrefly/pull/3415) | Negative narrowing for `isinstance` tuple targets. Phabricator landing. |
| **Vue** | [vue/core#14865](https://github.com/vuejs/core/pull/14865) | Skip idle persisted transition hooks in keep-alive moves. Runtime-core fix; ecosystem CI green across 16 suites. |
| **Apple** | [container#1559](https://github.com/apple/container/pull/1559) | Reject conflicting DNS flags in the CLI. |
| **Apple** | [coremltools#2700](https://github.com/apple/coremltools/pull/2700) | K-Means weight-palettization correctness — intra-cluster error, not centroid sums. |
| **Apple** | [password-manager#1094](https://github.com/apple/password-manager-resources/pull/1094) | Node.js CI validation for all 419 password-rule entries. |
| **Microsoft** | [rushstack#5805](https://github.com/microsoft/rushstack/pull/5805) | `package-deps-hash` handles Windows reserved names (`CON`, `PRN`, `NUL`) on `*nix` branches. |
| **Microsoft** | [rushstack#5804](https://github.com/microsoft/rushstack/pull/5804) | Lockfile warnings to stderr so piping stdout doesn't break. |
| **Hono** | [hono#4951](https://github.com/honojs/hono/pull/4951) | `compress` middleware respects `Accept-Encoding` exclusions. +8 tests. |
| **Jest** | [jest#16196](https://github.com/jestjs/jest/pull/16196) | Widened `toMatchObject` / `objectContaining` matcher signatures for class instances. |
| **NVIDIA** | [TransformerEngine#3065](https://github.com/NVIDIA/TransformerEngine/pull/3065) | Propagates `skip_fp8_weight_update` through `GroupedLinear` during FP8 CUDA graph capture, with a graphed-callables test. |
| **NVIDIA** | [apex#2003](https://github.com/NVIDIA/apex/pull/2003) | `type(x) == cls` → `isinstance` across fused optimizer, GDS, OpenFold Triton. |
| **Google** | [go-cloud#3727](https://github.com/google/go-cloud/pull/3727) | `memblob` Copy no longer aliases attributes between source and destination. Fourth go-cloud merge. |
| **Starlette** | [starlette#3317](https://github.com/Kludex/starlette/pull/3317) | `URL.replace()` no longer raises on a path-only URL when changing the port or credentials. |
| **OpenAI** | [agents-python#3485](https://github.com/openai/openai-agents-python/pull/3485) | Redacts raw failed JSON tool input from `ModelBehaviorError`. |

<sub>Smaller fixes across `apple/swift-nio`, `apple/servicetalk`, `apple/containerization`, `apple/foundationdb`, `ml-explore/mlx`, `NVIDIA/gpu-operator`, `NVIDIA/earth2studio`, `google/go-cloud`, `facebook/lexical`, `cloudflare/workers-sdk`, `denoland/deno`, `microsoft/rushstack`, `microsoft/PowerApps-Samples`.</sub>

<br/>

#### In review

A rolling set of fixes in review, each with a regression test that fails before and passes after.

| Org | PR | What it fixes |
|:---:|---|---|
| **Rust** | [rust#156787](https://github.com/rust-lang/rust/pull/156787) | Clarifies the `ArcInner::weak` lock-sentinel comment in `alloc`. Reviewer signed off, squashed, in queue. |
| **Deno** | [deno#34866](https://github.com/denoland/deno/pull/34866) | `deno test --doc` strips blockquote prefixes from quoted code blocks without corrupting non-blockquote lines. |
| **Fastify** | [fastify#6753](https://github.com/fastify/fastify/pull/6753) | `hasRequestDecorator` / `hasReplyDecorator` now see constructor-assigned built-in properties. Approved. |
| **Fastify** | [fastify-static#586](https://github.com/fastify/fastify-static/pull/586) | Pre-compressed responses set `Vary: Accept-Encoding` so shared caches keep variants separate. Approved. |
| **Vue** | [vue/core#14915](https://github.com/vuejs/core/pull/14915) | A plain `<template>` element now renders its children through `template.content` instead of dropping them. |
| **Cloudflare** | [workers-sdk#14176](https://github.com/cloudflare/workers-sdk/pull/14176) | `wrangler d1 execute` stops rejecting valid SQL that has `BEGIN TRANSACTION` inside a string or comment. |
| **TanStack** | [router#7612](https://github.com/TanStack/router/pull/7612) | `PathParamError` is re-exported from the React, Solid, and Vue router packages. |
| **Uvicorn** | [uvicorn#2989](https://github.com/Kludex/uvicorn/pull/2989) | `--reload` exclude dirs are respected even when an exact-name include matches. |
| **Charm** | [lipgloss#700](https://github.com/charmbracelet/lipgloss/pull/700) | Border size getters measure the real border width instead of returning a hardcoded 1. |
| **Valibot** | [valibot#1498](https://github.com/fabian-hiller/valibot/pull/1498) | ULID validation rejects overflowed timestamps by restricting the first character to 0-7. |
| **Hono** | [hono#5003](https://github.com/honojs/hono/pull/5003) | The lambda-edge adapter base64-encodes compressed bodies so gzipped responses are not corrupted. |
| **Jest** | [jest#16226](https://github.com/jestjs/jest/pull/16226) | `jest.spyOn` on an inherited getter or setter cleans up the own accessor on restore. |

<br/>

<!-- ============ THE STACK ============ -->

<img src="./header-stack.svg" alt="THE STACK" width="100%"/>

<br/>

<div align="center">

**`Languages`**
<br>
<img src="https://skillicons.dev/icons?i=python,ts,rust,go,swift,cpp,js&theme=dark" alt="Languages"/>

**`Frameworks`**
<br>
<img src="https://skillicons.dev/icons?i=fastapi,nextjs,react,nodejs,threejs,vite&theme=dark" alt="Frameworks"/>

**`Infra & Tools`**
<br>
<img src="https://skillicons.dev/icons?i=docker,mongodb,postgres,redis,gcp,linux,git,github&theme=dark" alt="Infra and Tools"/>

</div>

<br/>

<!-- ============ OFF THE COURT ============ -->

<img src="./header-court.svg" alt="OFF THE COURT" width="100%"/>

<div align="center">

<table>
<tr><td><b>Senior Patrol Leader</b></td><td>Boy Scouts. Troop of 40 to 50 scouts. Lead it.</td></tr>
<tr><td><b>Freshman Team Captain</b></td><td>Irvington HS varsity is next.</td></tr>
<tr><td><b>Lead CAD Designer</b></td><td>FTC Robotics. 3× regional finalist. Fusion 360.</td></tr>
<tr><td><b>Eagle Scout Projects</b></td><td>Two, led from proposal through completion.</td></tr>
<tr><td><b>Anthropic Academy</b></td><td>Agentic systems track. May 2026.</td></tr>
</table>

</div>

<br/>

<!-- ============ CONTACT ============ -->

<img src="./header-reach.svg" alt="CONTACT" width="100%"/>

<div align="center">

<br/>

<a href="https://github.com/LeSingh1"><img src="https://img.shields.io/badge/-github.com%2FLeSingh1-552583?style=for-the-badge&logo=github&logoColor=FDB927&labelColor=2d0f50" alt="GitHub" height="38"/></a>
&nbsp;
<a href="https://www.linkedin.com/in/shaurya-singh-b7591540b"><img src="https://img.shields.io/badge/-linkedin-552583?style=for-the-badge&logo=linkedin&logoColor=FDB927&labelColor=2d0f50" alt="LinkedIn" height="38"/></a>
&nbsp;
<a href="mailto:sshaurya914@gmail.com"><img src="https://img.shields.io/badge/-sshaurya914%40gmail.com-552583?style=for-the-badge&logo=gmail&logoColor=FDB927&labelColor=2d0f50" alt="Email" height="38"/></a>

<br/><br/>

<sub>Fremont, CA · Class of 2029</sub>

</div>
