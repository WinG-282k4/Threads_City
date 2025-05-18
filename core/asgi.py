"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import sys

print("ASGI Starting...")
print(f"DJANGO_SETTINGS_MODULE={os.environ.get('DJANGO_SETTINGS_MODULE', 'Not set')}")
print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
print(f"After setdefault: DJANGO_SETTINGS_MODULE={os.environ.get('DJANGO_SETTINGS_MODULE')}")

try:
    from django.core.asgi import get_asgi_application
    from channels.routing import ProtocolTypeRouter, URLRouter
    from channels.auth import AuthMiddlewareStack
    from thread.routing import websocket_urlpatterns

    application = ProtocolTypeRouter({
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        ),
    })
    print("ASGI application loaded successfully!")
except Exception as e:
    print(f"Error loading ASGI application: {e}")
    import traceback
    print(traceback.format_exc())
    raise
