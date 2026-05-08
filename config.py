"""
SalaryAxis — config.py
-----------------------
Central configuration. All API URLs, dataset IDs, and field mappings live here.
Production values are read from environment variables so the same codebase runs
locally, in Docker, on AWS ECS, and on GCP Cloud Run.

Author:  Shaz Moghaddam (Ethan Shahrooz Moghaddam) · London, UK
         https://github.com/ShazMoghaddam/salaryaxis
         shaz.moghaddam@gmail.com
Copyright (c) 2026 Shaz Moghaddam. Licensed under MIT.
"""

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env", override=False)
except ImportError:
    pass

# ---------------------------------------------------------------------------
# ONS Beta REST API
# ---------------------------------------------------------------------------
ONS_API_BASE = "https://api.ons.gov.uk/v1"

# ---------------------------------------------------------------------------
# NOMIS API — Annual Survey of Hours and Earnings (ASHE)
# ---------------------------------------------------------------------------
NOMIS_API_BASE  = "https://www.nomisweb.co.uk/api/v01"
ASHE_DATASET_ID = "NM_99_1"
BRES_DATASET_ID = "NM_189_1"
NOMIS_API_KEY   = os.getenv("NOMIS_API_KEY", "")

# NOMIS geography codes
NOMIS_GEO = {
    "UK":              "2092957699",
    "England":         "2092957698",
    "London":          "1937768322",
    "South East":      "1937768321",
    "North West":      "1937768318",
    "Yorkshire":       "1937768319",
    "West Midlands":   "1937768316",
    "East Midlands":   "1937768315",
    "East of England": "1937768314",
    "South West":      "1937768317",
    "North East":      "1937768313",
    "Scotland":        "1937768324",
    "Wales":           "1937768323",
}

# NOMIS measure codes for ASHE (NM_99_1)
NOMIS_MEASURES = {
    "median_gross_annual": "12",
    "mean_gross_annual":   "8",
    "median_hourly":       "13",
}

# NOMIS sex codes
NOMIS_SEX = {
    "all":    "7",
    "male":   "5",
    "female": "6",
}

# SOC 2020 occupation groups (1-digit)
SOC_MAJOR_GROUPS = {
    "1": "Managers, directors and senior officials",
    "2": "Professional occupations",
    "3": "Associate professional and technical occupations",
    "4": "Administrative and secretarial occupations",
    "5": "Skilled trades occupations",
    "6": "Caring, leisure and other service occupations",
    "7": "Sales and customer service occupations",
    "8": "Process, plant and machine operatives",
    "9": "Elementary occupations",
}

# ---------------------------------------------------------------------------
# Pipeline defaults
# ---------------------------------------------------------------------------
DEFAULT_YEAR = 2023
MIN_YEAR     = 2015

SALARY_MIN = 5_000
SALARY_MAX = 500_000

FORCE_PIPELINE_REFRESH = os.getenv("FORCE_PIPELINE_REFRESH", "false").lower() == "true"

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")

# ---------------------------------------------------------------------------
# Paid data source placeholders — activate by setting env vars
# ---------------------------------------------------------------------------
LINKEDIN_API_KEY      = os.getenv("LINKEDIN_API_KEY", "")
GLASSDOOR_API_KEY     = os.getenv("GLASSDOOR_API_KEY", "")
GLASSDOOR_PARTNER_ID  = os.getenv("GLASSDOOR_PARTNER_ID", "")
INDEED_PUBLISHER_ID   = os.getenv("INDEED_PUBLISHER_ID", "")

# ---------------------------------------------------------------------------
# Adzuna API — live UK job listings with salary data
# Free tier: 250 requests/day. Register at https://developer.adzuna.com
# ---------------------------------------------------------------------------
ADZUNA_APP_ID  = os.getenv("ADZUNA_APP_ID",  "")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY", "")
ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api/jobs/gb"

# Mapping from ONS SOC group labels to Adzuna search keywords
# Used to fetch live listings that correspond to each ONS occupation group
ADZUNA_SEARCH_TERMS = {
    "Managers, directors and senior officials":      "manager director senior manager",
    "Professional occupations":                       "analyst engineer professional",
    "Associate professional and technical occupations": "technician associate professional",
    "Administrative and secretarial occupations":    "administrator secretary admin",
    "Skilled trades occupations":                    "electrician plumber skilled trade",
    "Caring, leisure and other service occupations": "care worker nurse support worker",
    "Sales and customer service occupations":        "sales representative customer service",
    "Process, plant and machine operatives":         "machine operator production operative",
    "Elementary occupations":                        "warehouse operative delivery driver",
}
