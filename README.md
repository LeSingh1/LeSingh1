## Shaurya Singh

Builder working on AI applied to civic infrastructure and sports analytics. I like shipping hackathon projects that hold up when you scroll past the demo.

- Email — sshaurya914@gmail.com
- GitHub — [@LeSingh1](https://github.com/LeSingh1)

---

### Currently working on

- **[urbanmind-vision](https://github.com/LeSingh1/urbanmind-vision)** — Full-stack AI infrastructure planning simulator for growing cities. React + FastAPI + Claude + Mapbox, 50-year city simulation with a PPO reinforcement-learning agent (Stable Baselines3) and a constraint-validated road generator. Canonical base for the UrbanMind series.
- **[shotsense-scout](https://github.com/LeSingh1/shotsense-scout)** — MongoDB-powered NBA playoff shot-quality agent. Gemini + Google Cloud Agent Builder + MongoDB Atlas Vector Search.
- **[nba_shot_quality](https://github.com/LeSingh1/nba_shot_quality)** — Calibrated NBA xFG% model on the free `nba_api` playoff dataset. Methodology-first: GroupKFold, `TargetEncoder` inside the Pipeline, empirical-Bayes shrinkage, LogReg baseline.
- **[debate-skill](https://github.com/LeSingh1/debate-skill)** — Five-personality debate skill for Claude Code. Silent moderator + a judge that picks a winner.

### Recently merged

- **[apple/container#1559](https://github.com/apple/container/pull/1559)** — *Reject conflicting DNS flags* — Adds a `validate()` on the shared management option group so `container run` / `container create` refuse `--no-dns` together with `--dns`, `--dns-domain`, `--dns-option`, or `--dns-search`. Fixes [#1536](https://github.com/apple/container/issues/1536). Merged 2026-05-15.
- 25+ merged PRs on **nba_shot_quality** in May 2026 — 3D shot maps, top-down arc replays, real playoff data wiring, perf work (canvas-rendered shot dots replacing 10k+ SVG elements, code-splitting Three.js, lazy-loading 3.2 MB JSON off the critical path).

### Hackathon track record

The UrbanMind core (React + Zustand + Mapbox/MapLibre + Claude) is the shared spine across six competition entries. Same architecture, retargeted scenario data, different judging rubric each time.

| Project | Hackathon | Focus |
|---|---|---|
| [urbanmind-vision](https://github.com/LeSingh1/urbanmind-vision) | AI Autonomous Smart City Hackathon 2026 | 50-year city simulation with an RL agent |
| [civicops-planner](https://github.com/LeSingh1/civicops-planner) | Internal Tools Hacks | Internal city-planning dashboard |
| [citypilot-ai](https://github.com/LeSingh1/citypilot-ai) | Creator Colosseum 2025 | Startup pitch + feasibility tool |
| [civicplan-ai](https://github.com/LeSingh1/civicplan-ai) | HackAmerica 2025 — Civic Good | Civic infrastructure planner |
| [greengrid-ai](https://github.com/LeSingh1/greengrid-ai) | Tech to Treasure Environmental Hackathon | Climate resilience planner |
| [weatherready-ai](https://github.com/LeSingh1/weatherready-ai) | WeatherWise Hack | Extreme weather readiness |

Other one-off builds: [break-the-rules-basketball-v2](https://github.com/LeSingh1/break-the-rules-basketball-v2) (camera-controlled gesture basketball for Pixel Forge), [become-team-usa](https://github.com/LeSingh1/become-team-usa) (Team USA × Google Cloud archetype onboarding), [snapsell](https://github.com/LeSingh1/snapsell), [ewaste-detector](https://github.com/LeSingh1/ewaste-detector) (EcoLens — AI e-waste value detector).

### Stack I reach for

**Frontend** — React 18 · TypeScript · Vite · Zustand · Mapbox GL / MapLibre GL · D3 · Three.js / react-three-fiber
**Backend** — FastAPI · Python · Redis + RQ · Alembic · WebSockets · ReportLab
**AI** — Claude API (Anthropic SDK) · Gemini · Stable Baselines3 (PPO) · scikit-learn · Pydantic
**Infra** — Docker · MongoDB Atlas · Google Cloud Agent Builder

### How I work

- **State machine first.** Most of my apps share an `idle → analyzing → plan_ready → applying → complete` Zustand store. The UI is downstream of the state machine, not the other way around.
- **One canonical source of truth per project.** Scenario data lives in a single `data/*.ts` file. Editing one file should change the demo end-to-end.
- **Methodology over scoreboard chasing.** For ML work I default to leakage-resistant cross-validation, calibration, and shrinkage before tuning. Better to ship a calibrated baseline than an over-fit ensemble.
- **Polish is a feature.** Hero, empty states, loading shimmer, real screenshots — the demo is the deliverable.

### Open to

- Open-source contributions to developer-tooling projects in Swift, Rust, Python, and TypeScript. (Most recently: a parser-validation fix to [apple/container](https://github.com/apple/container).)
- Hackathon collaborations on civic-tech, climate, or sports-analytics problems.
- Internships and SWE roles in 2026 — AI infrastructure, applied ML, or product engineering.
