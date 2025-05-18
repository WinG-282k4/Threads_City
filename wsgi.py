"""
WSGI config for core project.
It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
import sys
print("WSGI Starting...")
print(f"DJANGO_SETTINGS_MODULE={os.environ.get('DJANGO_SETTINGS_MODULE', 'Not set')}")
print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
print(f"After setdefault: DJANGO_SETTINGS_MODULE={os.environ.get('DJANGO_SETTINGS_MODULE')}")

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    print("WSGI application loaded successfully!")
except Exception as e:
    print(f"Error loading WSGI application: {e}")
    import traceback
    print(traceback.format_exc())
    raise 