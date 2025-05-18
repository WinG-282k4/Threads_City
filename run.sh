#!/bin/bash
# Thiết lập biến môi trường Django
export DJANGO_SETTINGS_MODULE=core.settings
export PYTHONPATH=$PYTHONPATH:/opt/render/project/src

# Chạy daphne với cổng từ biến môi trường
exec daphne -b 0.0.0.0 -p $PORT core.asgi:application 