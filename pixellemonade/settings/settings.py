"""
Django settings for pixellemonade project.
"""
import os
import environ
from pathlib import Path

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env_path = environ.Path(__file__) - 3

# try to load the env file if there is one
try:
    environ.Env.read_env(env_path.file('.env'))
    print('read settings from .env')
except FileNotFoundError:
    print('No env file found')
    pass

STORAGES = {
    "original_files": "core.storages.PrivateStorage",
    "thumbnail_files": "core.storages.PublicStorage",
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')
HASHID_FIELD_SALT = env.str('HASHID_FIELD_SALT')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost'])
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])
API_HOSTNAME = env.str('API_HOSTNAME', default='http://127.0.0.1:8000/api/')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'imagekit',
    "django_unicorn",
    "debug_toolbar",

    'pixellemonade.core',
    'pixellemonade.api',
    'pixellemonade.cms',
]

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pixellemonade.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pixellemonade.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME', 'pixellemonade'),
        'USER': os.getenv('DB_USERNAME', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', "pass"),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', 5432),
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'hashid_field.BigHashidAutoField'

HASHID_FIELD_ENABLE_HASHID_OBJECT = False  # this is easier for the api schema stuff


CELERY_BROKER_URL= env.str('CELERY_BROKER_URL', 'amqp://rabbituser:rabbitpassword@localhost:5672//')
CELERY_TIMEZONE = "Australia/Tasmania"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

PUBLIC_S3_ENDPOINT_URL = env.str('PUBLIC_S3_ENDPOINT_URL')
PUBLIC_S3_ACCESS_KEY = env.str('PUBLIC_S3_ACCESS_KEY')
PUBLIC_S3_SECRET_KEY = env.str('PUBLIC_S3_SECRET_KEY')
PUBLIC_S3_BUCKET_NAME = env.str('PUBLIC_S3_BUCKET_NAME')
PUBLIC_S3_CUSTOM_DOMAIN_NAME = env.str('PUBLIC_S3_CUSTOM_DOMAIN_NAME', None)

PRIVATE_S3_ENDPOINT_URL = env.str('PRIVATE_S3_ENDPOINT_URL')
PRIVATE_S3_ACCESS_KEY = env.str('PRIVATE_S3_ACCESS_KEY')
PRIVATE_S3_SECRET_KEY = env.str('PRIVATE_S3_SECRET_KEY')
PRIVATE_S3_BUCKET_NAME = env.str('PRIVATE_S3_BUCKET_NAME')
PRIVATE_S3_CUSTOM_DOMAIN_NAME = env.str('PRIVATE_S3_CUSTOM_DOMAIN_NAME', None)

INTERNAL_IPS = env.list('INTERNAL_IPS', default=["127.0.0.1"])
