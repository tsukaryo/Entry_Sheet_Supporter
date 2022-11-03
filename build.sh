#!/usr/bin/env bash# exit on errorset -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-inputpython manage.py migrate