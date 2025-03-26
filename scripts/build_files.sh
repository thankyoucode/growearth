#!/bin/bash
# scripts/build_files.sh

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput --clear
