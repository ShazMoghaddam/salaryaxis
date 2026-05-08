"""
gunicorn.conf.py
-----------------
Production Gunicorn configuration for the SalaryAxis.

Tuning philosophy
-----------------
  workers    = (2 × CPU cores) + 1   — standard recommendation for I/O-bound apps
  threads    = 2                       — each worker handles 2 concurrent requests
  worker_class = gthread               — threaded (suits Flask's request model)
  timeout    = 120 s                  — allows the slow-path pipeline run on cold start

Environment overrides
---------------------
All values can be overridden via environment variables at runtime:
  GUNICORN_WORKERS   GUNICORN_THREADS   GUNICORN_TIMEOUT   PORT
"""

import multiprocessing
import os

# ── Binding ───────────────────────────────────────────────────────────────────
host = os.getenv("HOST", "0.0.0.0")
port = os.getenv("PORT", "8000")
bind = f"{host}:{port}"

# ── Workers ───────────────────────────────────────────────────────────────────
# Start conservative (2 workers) on free-tier cloud instances (1 vCPU / 512 MB).
# Scale up via env var once you've verified memory headroom.
workers     = int(os.getenv("GUNICORN_WORKERS", max(2, multiprocessing.cpu_count() * 2 + 1)))
threads     = int(os.getenv("GUNICORN_THREADS", "2"))
worker_class = "gthread"

# ── Timeouts ──────────────────────────────────────────────────────────────────
# 120 s allows the DataService slow path (full NOMIS API run) on first boot.
# Subsequent requests are served from CSV cache and are < 1 s.
timeout       = int(os.getenv("GUNICORN_TIMEOUT", "120"))
graceful_timeout = 30
keepalive     = 5

# ── Logging ───────────────────────────────────────────────────────────────────
loglevel     = os.getenv("LOG_LEVEL", "info").lower()
accesslog    = "-"       # stdout  → captured by cloud logging agents
errorlog     = "-"       # stderr
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" %(D)s μs'

# ── Process naming ────────────────────────────────────────────────────────────
proc_name = "salaryaxis"

# ── Security ──────────────────────────────────────────────────────────────────
# Limit request line + header sizes to reduce header-injection risk.
limit_request_line       = 4094
limit_request_fields     = 100
limit_request_field_size = 8190

# ── Preloading ────────────────────────────────────────────────────────────────
# preload_app = True loads the app once in the master process before forking.
# Disabled here because DataService.initialise() makes network calls that
# should happen per-worker, not in the master.
preload_app = False
