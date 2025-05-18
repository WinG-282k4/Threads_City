#!/bin/bash
# Thiết lập biến môi trường Django
export DJANGO_SETTINGS_MODULE=core.settings

# Chạy gunicorn với cổng từ biến môi trường
gunicorn --bind 0.0.0.0:$PORT core.wsgi:application --config gunicorn_config.py 