"""
Django settings for config project.
"""

from pathlib import Path
import os

# ======================
# BASE DIRECTORY
# ======================

BASE_DIR = Path(__file__).resolve().parent.parent


# ======================
# SECURITY
# ======================

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-dev-key-change-in-production"
)

DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = ["*"]


# ======================
# APPLICATIONS
# ======================

INSTALLED_APPS = [
    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'corsheaders',
    'cloudinary',
    'cloudinary_storage',

    # Local apps
    'movies',
]


# ======================
# MIDDLEWARE
# ======================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    # CORS MUST BE BEFORE CommonMiddleware
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ======================
# URLS / TEMPLATES
# ======================

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# ======================
# DATABASE (SQLITE)
# ======================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ======================
# PASSWORD VALIDATION
# ======================

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ======================
# INTERNATIONALIZATION
# ======================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# ======================
# STATIC FILES
# ======================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"


# ======================
# CLOUDINARY (MEDIA STORAGE)
# ======================

import cloudinary
import cloudinary.uploader
import cloudinary.api

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.environ.get("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.environ.get("CLOUDINARY_API_KEY"),
    "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET"),
}

# 🔴 IMPORTANT: Cloudinary MUST be the only media backend
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# ❌ DO NOT define MEDIA_URL or MEDIA_ROOT
# They BREAK Cloudinary if present


# ======================
# CORS / CSRF
# ======================

CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "http://127.0.0.1",
    "https://*.onrender.com",
]


# ======================
# DEFAULT PRIMARY KEY
# ======================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ======================
# AUTO CREATE SUPERUSER (RENDER FREE PLAN)
# ======================

if os.environ.get("DJANGO_SUPERUSER_USERNAME"):
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()

        if not User.objects.filter(
            username=os.environ["DJANGO_SUPERUSER_USERNAME"]
        ).exists():
            User.objects.create_superuser(
                username=os.environ["DJANGO_SUPERUSER_USERNAME"],
                email=os.environ.get("DJANGO_SUPERUSER_EMAIL"),
                password=os.environ["DJANGO_SUPERUSER_PASSWORD"],
            )
    except Exception:
        pass
    