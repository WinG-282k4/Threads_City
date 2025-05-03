import os
import sys
import django
from django.core.asgi import get_asgi_application

# Thiết lập biến môi trường cho Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Khởi tạo Django
django.setup()

# Import daphne và chạy server
if __name__ == "__main__":
    from daphne.cli import CommandLineInterface
    sys.argv = ["daphne", "-b", "0.0.0.0", "-p", "8000", "core.asgi:application"]
    CommandLineInterface.entrypoint() 