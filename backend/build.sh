#!/usr/bin/env bash
# اسکریپت Build و آماده سازی Django
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

