# -*- coding: utf-8 -*-

import environ

base_dir = environ.Path(__file__) - 2

# Read env file
env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(base_dir('env'))

INSTALLED_APPS = [
    # Local
    'apps.userprofile',
    'apps.lan',
    'apps.news',
    'apps.sponsor',

    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'rest_framework_swagger',
    'mozilla_django_oidc',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'core.catch_auth.FredOIDCAB',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [base_dir('templates')],
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

# General
BASE_DIR = base_dir
DEBUG = env('DEBUG')
TEMPLATE_DEBUG = DEBUG
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = env('ALLOWED_HOSTS')
SITE_NAME = env('SITE_NAME')
WSGI_APPLICATION = 'core.wsgi.application'
ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Database
DATABASES = {
    'default': env.db('DATABASE_URL'),
}

# Email
DEFAULT_MAIL = env('DEFAULT_MAIL', default='app@localhost')
SUPPORT_MAIL = env('SUPPORT_MAIL', default='support@localhost')
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
# Mailgun
MAILGUN_ACCESS_KEY = env('MAILGUN_ACCESS_KEY', default='')
MAILGUN_SERVER_NAME = env('MAILGUN_SERVER_NAME', default='')

# Security
CSRF_COOKIE_PATH = '/'
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = env('CSRF_COOKIE_SECURE', default=True)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = env('SESSION_COOKIE_SECURE', default=True)
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = base_dir('static')

# i18n
LANGUAGE_CODE = 'en-us'
TIME_ZONE = env('TIME_ZONE', default='UTC')
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] [%(levelname)s] %(message)s',
        },
    },
    'handlers': {
        'error_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': base_dir(env('LOG_DIR', default='log'), 'error.log'),
            'maxBytes': 5 * 1024 * 1024,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['error_file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# OIDC
OIDC_RP_CLIENT_ID = env('OIDC_RP_CLIENT_ID', default='')
OIDC_RP_CLIENT_SECRET = env('OIDC_RP_CLIENT_SECRET', default='')
OIDC_OP_AUTHORIZATION_ENDPOINT = env('OIDC_OP_AUTHORIZATION_ENDPOINT', default='')
OIDC_OP_TOKEN_ENDPOINT = env('OIDC_OP_TOKEN_ENDPOINT', default='')
OIDC_OP_USER_ENDPOINT = env('OIDC_OP_USER_ENDPOINT', default='')
OIDC_RP_SIGN_ALGO = env('OIDC_RP_SIGN_ALGO', default='')
OIDC_OP_JWKS_ENDPOINT = env('OIDC_OP_JWKS_ENDPOINT', default='')

# DRF
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'mozilla_django_oidc.contrib.drf.OIDCAuthentication',
    ],
}

# Swagger
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'oauth': {
            'type': 'oauth2',
            'flow': 'accessCode',
            'authorizationUrl': env('OIDC_OP_AUTHORIZATION_ENDPOINT', default=''),
            'tokenUrl': env('OIDC_OP_TOKEN_ENDPOINT', default=''),
        },
    },
    'USE_SESSION_AUTH': False,
}
