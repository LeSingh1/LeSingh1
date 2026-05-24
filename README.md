<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:161b22,100:0d1117&height=120&section=header" width="100%" />

# Hi, I'm Shaurya 👋
Builder. Civic-tech + sports analytics + a lot of open source.

<p align="center">
  <a href="mailto:sshaurya914@gmail.com"><img src="https://img.icons8.com/color/48/gmail-new.png" width="32" alt="Email"/></a>
  <a href="https://github.com/LeSingh1"><img src="https://cdn.simpleicons.org/github/e6edf3" width="32" alt="GitHub"/></a>
</p>
</div>
<br>

## 🛠️ Open Source

Active multi-repo contributor across foundational tooling. ~48 PRs merged, ~50 in review across **Apple, Microsoft, NVIDIA, OpenAI, Google, Meta, Vercel, Stripe, Shopify, Cloudflare, HuggingFace,** and the major language/framework repos.

### Substantive landings

| PR | What it fixes |
|---|---|
| [apple/container#1559](https://github.com/apple/container/pull/1559) | Reject conflicting DNS flags in `container run`/`create` (fixes #1536) |
| [apple/coremltools#2700](https://github.com/apple/coremltools/pull/2700) | `_EfficientKMeans` cluster reduction now uses intra-cluster errors (fixes #2698) |
| [microsoft/rushstack#5805](https://github.com/microsoft/rushstack/pull/5805) | `package-deps-hash` skips Windows reserved device names (fixes #5604) |
| [microsoft/rushstack#5804](https://github.com/microsoft/rushstack/pull/5804) | Route `lockfile-changed` warning to stderr (fixes #5406) |
| [honojs/hono#4951](https://github.com/honojs/hono/pull/4951) | `compress` middleware respects Accept-Encoding when encoding option is set |
| [jestjs/jest#16196](https://github.com/jestjs/jest/pull/16196) | `toMatchObject` / `objectContaining` accept class instances |
| [openai/openai-agents-python#3485](https://github.com/openai/openai-agents-python/pull/3485) | Redact invalid JSON payload in `ModelBehaviorError` data |
| [NVIDIA/apex#2003](https://github.com/NVIDIA/apex/pull/2003) | Fix `E721` type comparisons across the codebase |

Plus targeted fixes/docs in **apple/swift-nio, apple/servicetalk, apple/containerization, apple/foundationdb, apple/password-manager-resources, NVIDIA/TransformerEngine, NVIDIA/earth2studio, NVIDIA/gpu-operator, ml-explore/mlx, google/go-cloud, facebook/lexical, cloudflare/workers-sdk, openai/openai-agents-python**.

### In review

Open PRs across **python/cpython, rust-lang/rust, rust-lang/rust-analyzer, denoland/deno, denoland/std, vuejs/core, solidjs/solid, python/mypy, sqlalchemy/sqlalchemy, evanw/esbuild, vitest-dev/vitest, trpc/trpc, TanStack/query, drizzle-team/drizzle-orm, vercel/ai, vercel/satori, vercel/swr, huggingface/datasets, simonw/sqlite-utils, apple/coremltools (4), microsoft/fluentui, microsoft/microsoft-ui-xaml, microsoft/PowerApps-Samples, stripe/react-stripe-js, stripe/smokescreen, stripe/skycfg, Shopify/draggable, Shopify/hydrogen, facebook/openzl, facebook/idb, NVIDIA/Megatron-LM, NVIDIA/earth2studio, openai/evals, openai/whisper, openai/openai-node, openai/openai-cookbook, openai/tiktoken, openai/shap-e, openai/transformer-debugger, openai/openai-realtime-console, openai/openai-realtime-agents**.

## 🚀 Current Builds

- **[edgeboard](https://github.com/LeSingh1/edgeboard)** — Personal real-time PrizePicks board + lineup optimizer. Real player projections (MLB Stats API, ESPN), live in-game stats, accurate Power/Flex multipliers, correlation-aware Smart Suggest.
- **[urbanmind-vision](https://github.com/LeSingh1/urbanmind-vision)** — Full-stack AI infrastructure planning simulator. React + FastAPI + Claude + Mapbox, 50-year city simulation with a PPO RL agent (Stable Baselines3) and a constraint-validated road generator. Canonical base for the UrbanMind series.
- **[shadowbuyer](https://github.com/LeSingh1/shadowbuyer)** — Autonomous B2B procurement agent swarm. Adversarial negotiator (Qwen3-Max vs GLM-5.1) routed through TokenRouter, deployed on Zeabur.
- **[shotsense-scout](https://github.com/LeSingh1/shotsense-scout)** — MongoDB-powered NBA playoff shot-quality agent. Gemini + Google Cloud Agent Builder + MongoDB Atlas Vector Search.
- **[nba_shot_quality](https://github.com/LeSingh1/nba_shot_quality)** — Calibrated NBA xFG% model on the free `nba_api` playoff dataset. Methodology-first: GroupKFold, `TargetEncoder` inside the Pipeline, empirical-Bayes shrinkage, LogReg baseline. Production-grade frontend with canvas shot maps and Three.js arc replays.

## 🏆 Hackathon Series

The UrbanMind core (React + Zustand + Mapbox/MapLibre + Claude) is the shared spine across six entries — same architecture, retargeted scenario data, different rubric.

| Project | Hackathon | Focus |
|---|---|---|
| [urbanmind-vision](https://github.com/LeSingh1/urbanmind-vision) | AI Autonomous Smart City Hackathon 2026 | 50-year city simulation with an RL agent |
| [civicops-planner](https://github.com/LeSingh1/civicops-planner) | Internal Tools Hacks | Internal city-planning dashboard |
| [citypilot-ai](https://github.com/LeSingh1/citypilot-ai) | Creator Colosseum 2025 | Startup pitch + feasibility tool |
| [civicplan-ai](https://github.com/LeSingh1/civicplan-ai) | HackAmerica 2025 — Civic Good | Civic infrastructure planner |
| [greengrid-ai](https://github.com/LeSingh1/greengrid-ai) | Tech to Treasure Environmental Hackathon | Climate resilience planner |
| [weatherready-ai](https://github.com/LeSingh1/weatherready-ai) | WeatherWise Hack | Extreme weather readiness |
| [shadowbuyer](https://github.com/LeSingh1/shadowbuyer) | Procurement agent hack | Adversarial B2B agent swarm |

## How I work

- **State machine first.** Most of my apps share an `idle → analyzing → plan_ready → applying → complete` Zustand store. UI is downstream of state, not the other way around.
- **One canonical data file per project.** Scenario data lives in a single `data/*.ts`. Editing one file changes the demo end-to-end.
- **Methodology over scoreboard chasing.** For ML I default to leakage-resistant CV, calibration, and shrinkage before tuning. Calibrated baseline > overfit ensemble.
- **Polish is a feature.** Hero, empty states, loading shimmer, real screenshots — the demo is the deliverable.

## Stack

<div align="center">

**`Languages`**
<br>
<img src="https://skillicons.dev/icons?i=python,ts,rust,go,swift,cpp,js" />

**`Frameworks`**
<br>
<img src="https://skillicons.dev/icons?i=fastapi,nextjs,react,nodejs,threejs,vite" />

**`Infra & Tools`**
<br>
<img src="https://skillicons.dev/icons?i=docker,mongodb,postgres,redis,gcp,linux,git,github" />

<br>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:161b22,100:0d1117&height=100&section=footer" width="100%" />
</div>
