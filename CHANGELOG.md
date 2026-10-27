# Changelog — SalaryAxis

Developed by Shaz Moghaddam (Ethan Shahrooz Moghaddam) · London, UK
https://github.com/ShazMoghaddam/salaryaxis

All notable changes documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### Added

- GitHub Actions CI workflow (`.github/workflows/ci.yml`) on Python 3.12: installs
  requirements, compiles all Python files, lints for errors with ruff, loads `config.py`,
  and validates the Docker Compose files and demo CSV. Test suite and Docker build jobs
  to follow once the application source is restored.
- CI status badge in the README.

---

## [1.0.0] — 2026 — Initial Release

### Phase 7 — GDPR Compliance & Paid Source Integration

- `api/middleware/gdpr.py` — IPv4/IPv6 anonymisation, structured JSON audit logging,
  `scrub_pii()` recursive cleaner, `GDPRMiddleware` Flask hooks, 6 security response headers
- `api/routes/consent.py` — `GET /consent/status`, `POST /consent/record`, `GET /privacy`
- `data/sources/paid_sources.py` — `LinkedInSource`, `GlassdoorSource`, `IndeedSource`
  with `PaidDataSource` interface and 70/30 ONS-blend algorithm. `PaidSourceRegistry`
  auto-detects configured sources.
- `frontend/src/components/ConsentBanner.jsx` — GDPR-compliant banner, privacy modal
- `frontend/src/pages/Privacy.jsx` — live policy from API, consent toggle controls
- Health endpoint updated with GDPR status and paid source configuration
- Privacy & Data link added to Sidebar
- 65 new tests (232 total)

### Phase 6 — Cloud Deployment

- Multi-stage `Dockerfile` (Node 20 → React build → Python 3.12 slim + Gunicorn)
- `docker-compose.yml` (dev) and `docker-compose.prod.yml` (nginx + API)
- `nginx/nginx.conf` — SSL, gzip, security headers, upstream proxy
- `gunicorn.conf.py` — production tuning
- `Makefile` — 20 convenience commands
- `deploy/aws/` — ECS Fargate task definition, rolling deploy, IAM policy
- `deploy/gcp/` — Cloud Run YAML, deploy script
- `deploy/setup/` — one-time infrastructure setup (ECR, ECS, Artifact Registry)
- `.github/workflows/` — CI, AWS deploy, GCP deploy
- `config.py` fully env-var aware; `api/__init__.py` configurable CORS + Redis rate limiting
- `deploy/DEPLOYMENT.md` — full step-by-step guide with cost estimates
- 69 new tests (167 total)

### Phase 5 — Frontend Integration

- `context/AppContext.jsx` — global state, single health check, shared occupations/regions
- `components/ErrorBoundary.jsx`, `AppLoading.jsx`, `Toast.jsx`, `ExportButton.jsx`,
  `ChartTooltip.jsx`
- `pages/NotFound.jsx`
- All pages upgraded: context reads, CSV export, shareable URL params (Benchmark),
  box-plot visual (Occupations), gap % chart (GenderGap)
- Flask SPA catch-all correctly excludes `/api/*` paths

### Phase 4 — Frontend UI

- React 18 + Vite in `frontend/`
- Design system: dark editorial (`#0e1117` + `#f5a623` amber), DM Serif / DM Sans / DM Mono
- `services/api.js`, `hooks/useApi.js`
- Components: `Sidebar`, `StatCard`, `SalaryRangeBar`
- Pages: Dashboard, Benchmark, Trends, Occupations, Regions, GenderGap

### Phase 3 — Backend REST API

- Flask app factory with CORS, Flask-Limiter, blueprints
- `api/services/data_service.py` — singleton, fast CSV / slow pipeline load
- Middleware: `error_handlers.py`, `validators.py`
- 9 API endpoints across 5 route blueprints
- `wsgi.py` production entry point
- 47 new tests (97 total)

### Phase 2 — Data Processing & Analysis

- `data/cpi_fetcher.py` — CPIH rates, cumulative price index, `adjust_for_inflation()`
- `pipeline/analyser.py` — distributions, Shapiro-Wilk normality, Tukey IQR outliers,
  real salary trends, CAGR, sector aggregation
- `pipeline/benchmarker.py` — occupation lookup, regional multipliers, experience levels,
  fairness verdict with gap calculation
- `pipeline/gender_analyser.py` — ONS-standard pay gap formula, YoY trends
- 31 new tests (51 total)

### Phase 1 — Data Foundation & ONS Integration

- `config.py` — NOMIS/ONS endpoints, SOC codes, geography codes
- `data/ons_fetcher.py` — ASHE by occupation, time series, by region; disk cache
- `pipeline/processor.py` — validate → normalise → enrich → aggregate → export
- `main.py` — CLI with Rich console output
- `utils/logger.py` — Rich logging
- 20 tests
