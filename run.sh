#!/bin/bash
# Thiết lập biến môi trường Django
export DJANGO_SETTINGS_MODULE=core.settings

# Chạy daphne với cổng từ biến môi trường
daphne -b 0.0.0.0 -p $PORT core.asgi:application 