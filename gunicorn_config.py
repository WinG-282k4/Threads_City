"""
Gunicorn configuration file
"""

import os
import multiprocessing

# Thiết lập biến môi trường
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Thông số cấu hình
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 50
accesslog = "-"
errorlog = "-"
loglevel = "info"
limit_request_line = 0
limit_request_fields = 100

# Debug
print(f"Starting Gunicorn with:")
print(f"  - DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
print(f"  - Bind: {bind}")
print(f"  - Workers: {workers}")
print(f"  - Worker class: {worker_class}") 