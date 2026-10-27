# SalaryAxis

**A professional-grade UK salary intelligence platform** — built on ONS open data,
deployable to AWS or GCP, and fully GDPR-compliant.

Developed by **[Shaz Moghaddam](https://shazmoghaddam.github.io)** · London, UK

[![CI](https://github.com/ShazMoghaddam/salaryaxis/actions/workflows/ci.yml/badge.svg)](https://github.com/ShazMoghaddam/salaryaxis/actions/workflows/ci.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://python.org)
[![React 18](https://img.shields.io/badge/react-18-61DAFB.svg)](https://reactjs.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GDPR Compliant](https://img.shields.io/badge/GDPR-compliant-green.svg)](#gdpr-compliance)

> **Repository status:** this repo currently holds the configuration, entry points and
> documentation only. The application source (`api/`, `data/`, `pipeline/`, `frontend/`,
> `tests/`, `deploy/`) is being restored and will be added in a later release. Until then,
> the Quick Start below will not run from a fresh clone. CI currently checks the files that
> are here (Python compiles, config loads, Compose files and demo data are valid).

---

## Overview

SalaryAxis aggregates UK salary data from the Office for National Statistics, applies
statistical analysis and CPI inflation adjustment, and delivers fair salary benchmarks
through a clean REST API and a polished React dashboard. Built to production standards —
multi-stage Docker, zero-downtime ECS deploy, GDPR-compliant consent system.

---

## Features

| Feature | Description |
|---------|-------------|
| **Salary Benchmark** | Fair salary range for any UK occupation, adjusted for region and experience. Verdict: fair / underpaid / above market. |
| **Inflation-Adjusted Trends** | Nominal and CPI-adjusted real salary growth 2015–2023. |
| **Occupation Profiles** | Full distribution stats (P10–P90, IQR, skewness) per SOC group. |
| **Regional Analysis** | Median pay by UK region with live ONS cost-of-living multipliers. |
| **Gender Pay Gap** | ONS-standard pay gap by occupation and region, 2015–2023 trend. |
| **CAGR Analysis** | Compound annual growth rates in real and nominal terms. |
| **CSV Export** | Every dataset downloadable as a timestamped CSV. |
| **Shareable Benchmarks** | URL-encoded results — share a benchmark link with anyone. |
| **GDPR Compliant** | No personal data collected. IP anonymised. Full privacy policy API. |
| **Paid Source Ready** | LinkedIn, Glassdoor, Indeed stubs — activate via environment variables. |

---

## Data Sources

All data sourced from **ONS open datasets** under the Open Government Licence v3.0.

| Source | Dataset | Licence |
|--------|---------|---------|
| ONS NOMIS | Annual Survey of Hours and Earnings (ASHE) — NM_99_1 | OGL v3.0 |
| ONS Beta API | Consumer Prices Index (CPIH) — series D7BT | OGL v3.0 |

---

## Quick Start

```bash
git clone https://github.com/ShazMoghaddam/salaryaxis.git
cd salaryaxis
make install
python main.py          # fetch ONS data → output/*.csv
make dev-api            # Terminal 1: Flask :8080
make dev-ui             # Terminal 2: React :3000
```

These steps need the full application source, which is being restored (see the status note above).

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/health` | Liveness + GDPR + paid source status |
| `GET` | `/api/v1/occupations` | SOC 2020 groups with salary stats |
| `GET` | `/api/v1/salary/benchmark` | Fair salary range recommendation |
| `GET` | `/api/v1/salary/trends` | Nominal + real trends 2015–2023 |
| `GET` | `/api/v1/regions` | Median salary by UK region |
| `GET` | `/api/v1/gender-gap` | Gender pay gap by occupation or region |
| `GET` | `/api/v1/analysis/distribution` | Full distribution stats |
| `GET` | `/api/v1/analysis/cagr` | Compound annual growth rates |
| `GET` | `/api/v1/consent/status` | GDPR consent requirements |
| `POST` | `/api/v1/consent/record` | Record consent decision |
| `GET` | `/api/v1/privacy` | Machine-readable privacy policy |

---

## Project Structure

What is in this repository today:

```
salaryaxis/
├── config.py · main.py · wsgi.py · gunicorn.conf.py · __init__.py
├── Makefile · requirements.txt
├── Dockerfile · docker-compose.yml · docker-compose.prod.yml
├── .github/workflows/ci.yml
├── salaryaxis_demo_org.csv
├── SalaryAxis-ExecutiveSummary.pdf · SalaryAxis-PitchDeck.pptx
└── README.md · CHANGELOG.md · LICENSE
```

---

## Makefile Reference

```bash
make install     make test        make dev-api     make dev-ui
make build       make build-docker make deploy-aws  make deploy-gcp
make pipeline    make clean       make health
```

---

## GDPR Compliance

No personal data collected. Salary calculator runs client-side.
IP anonymised (last octet stripped). 30-day log retention.
Full privacy policy at `/api/v1/privacy`.

---

## Tech Stack

Python 3.12 · Flask 3 · Gunicorn · Pandas · NumPy · SciPy ·
React 18 · Vite · Recharts · Docker · nginx · GitHub Actions ·
AWS ECS Fargate or GCP Cloud Run · ONS open data

---

## Author

**Shaz Moghaddam** (Ethan Shahrooz Moghaddam) — London, UK

🌐 [shazmoghaddam.github.io](https://shazmoghaddam.github.io) ·
💼 [linkedin.com/in/shazmoghaddam](https://www.linkedin.com/in/shazmoghaddam/) ·
🐙 [github.com/ShazMoghaddam](https://github.com/ShazMoghaddam) ·
📧 [shaz.moghaddam@gmail.com](mailto:shaz.moghaddam@gmail.com)

---

## Licence

MIT — see [LICENSE](LICENSE).
Copyright © 2026 Shaz Moghaddam (Ethan Shahrooz Moghaddam).

Data from the ONS is licensed under the
[Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).
