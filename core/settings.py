"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']  # Sẽ được cập nhật với domain của PythonAnywhere


# Application definition

INSTALLED_APPS = [
    "thread.apps.ThreadConfig",
    "accounts.apps.AccountsConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sorl.thumbnail",
    "rest_framework",
    "corsheaders",
    "channels",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv('DB_NAME'),
        "USER": os.getenv('DB_USERNAME'),
        "PASSWORD": os.getenv('DB_PASSWORD'),
        "HOST": os.getenv('DB_HOST'),
        "PORT": os.getenv('DB_PORT', '3306'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Yangon"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files (Uploaded files)
MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

if DEBUG:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
            "LOCATION": "127.0.0.1:11211",
        }
    }

# Deployment security stuff
if not DEBUG:
    SECURE_HSTS_SECONDS = 3600
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    CONN_MAX_AGE = 3600

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# CSRF settings
CSRF_COOKIE_NAME = 'csrftoken'  # Tên của cookie
CSRF_USE_SESSIONS = False  # Token lưu trong cookie
CSRF_COOKIE_HTTPONLY = False  # Client JS có thể đọc được cookie
CSRF_COOKIE_SAMESITE = 'None'  # Allow cross-site requests
CSRF_COOKIE_SECURE = True  # Only send over HTTPS

CSRF_TRUSTED_ORIGINS = [
    'https://wing2k4.pythonanywhere.com',
    'http://wing2k4.pythonanywhere.com',
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'https://www.postman.com',
    'https://v0-clone-threads.vercel.app',
    'https://thread-clone.onrender.com'
]

# CORS settings

CSRF_COOKIE_NAME = 'csrftoken'  # Tên của cookie
CSRF_USE_SESSIONS = False  # Token lưu trong cookie
CSRF_COOKIE_HTTPONLY = False  # Client JS có thể đọc được cookie
CSRF_COOKIE_SAMESITE = 'None'  # Allow cross-site requests
CSRF_COOKIE_SECURE = True  # Only send over HTTPS

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Frontend development server
    "http://127.0.0.1:5173",
    "http://localhost:8000",  # Django server
    "http://127.0.0.1:8000", 
    "https://wing2k4.pythonanywhere.com",
    "http://wing2k4.pythonanywhere.com",
    "https://www.postman.com",
    "https://v0-clone-threads.vercel.app",
    "https://thread-clone.onrender.com"
]

CORS_ALLOW_CREDENTIALS = True  # Allow sending credentials (cookies)

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'referer',
]

# CSRF settings for API
CSRF_EXEMPT_URLS = [
    '/api/users/$',  # Only exact registration endpoint
    '/api/threads/$',  # Only exact threads endpoint
    '/api/auth/users/forgot_password/$',  # Forgot password endpoint
]

# Cookie settings
SESSION_COOKIE_SAMESITE = 'None'  # Allow cross-site cookies
SESSION_COOKIE_SECURE = True  # Only send over HTTPS
CSRF_COOKIE_SAMESITE = 'None'  # Allow cross-site cookies
CSRF_COOKIE_SECURE = True  # Only send over HTTPS

# Channel layers for WebSockets
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# Cấu hình Pusher - đọc từ biến môi trường
PUSHER_APP_ID = os.getenv('PUSHER_APP_ID')
PUSHER_KEY = os.getenv('PUSHER_KEY')
PUSHER_SECRET = os.getenv('PUSHER_SECRET')
PUSHER_CLUSTER = os.getenv('PUSHER_CLUSTER')

# Kiểm tra nếu đang chạy trên PythonAnywhere
ON_PYTHONANYWHERE = 'PYTHONANYWHERE_SITE' in os.environ
USE_PUSHER = ON_PYTHONANYWHERE

# Nếu đang chạy trên môi trường local, bạn có thể chọn sử dụng Channels hoặc Pusher
if not ON_PYTHONANYWHERE:
    INSTALLED_APPS += ['channels']
    ASGI_APPLICATION = "core.asgi.application"

    # Cấu hình Channels
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer"
        }
    }

print("▶ Using DB HOST:", os.getenv("DB_HOST"))

# Email Configuration
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
