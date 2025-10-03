#!/bin/bash

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations (if needed in future)
# python -m alembic upgrade head

# Start Gunicorn with Uvicorn workers
gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 --timeout 120 app.main:app
