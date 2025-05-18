#!/bin/bash
# Thiết lập biến môi trường Django
export DJANGO_SETTINGS_MODULE=core.settings
export PYTHONPATH=$PYTHONPATH:/opt/render/project/src

# Chạy gunicorn với cổng từ biến môi trường
exec gunicorn --bind 0.0.0.0:$PORT core.wsgi:application 