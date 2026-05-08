"""
SalaryAxis — wsgi.py
---------------------
Production WSGI entry point.

Development:
    python3 wsgi.py
    Open http://localhost:8080

Production (Gunicorn):
    gunicorn 'wsgi:app' --workers 2 --bind 0.0.0.0:8000

Author:  Shaz Moghaddam · https://github.com/ShazMoghaddam/salaryaxis
Copyright (c) 2026 Shaz Moghaddam. Licensed under MIT.
"""

import os
from utils.logger import setup_logging
from api import create_app

setup_logging(os.getenv("LOG_LEVEL", "INFO"))

app = create_app()

if __name__ == "__main__":
    port  = int(os.getenv("PORT", 8080))
    host  = os.getenv("HOST", "0.0.0.0")
    debug = os.getenv("FLASK_ENV", "production") == "development"
    app.run(host=host, port=port, debug=debug)
