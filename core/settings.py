import os
import environ

root = environ.Path(__file__) - 2
BASE_DIR = root()

env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(BASE_DIR + '/env')

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

    # Thirdparty
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
        'DIRS': [BASE_DIR + '/templates']
        ,
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
DEBUG = env('DEBUG')
TEMPLATE_DEBUG = DEBUG
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = env('ALLOWED_HOSTS')
SITE_NAME = env('SITE_NAME')
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR + '/static'
WSGI_APPLICATION = 'core.wsgi.application'
ROOT_URLCONF = 'core.urls'
LOGIN_REDIRECT_URL = 'http://localhost:8000'
LOGOUT_REDIRECT_URL = 'http://localhost:8000'

# Database
DATABASES = {
    'default': env.db('DATABASE_URL')
}

# Email
DEFAULT_MAIL = env('DEFAULT_MAIL')
SUPPORT_MAIL = env('SUPPORT_MAIL')
EMAIL_BACKEND = env('EMAIL_BACKEND')
# Mailgun (https://pypi.org/project/django-mailgun/)
MAILGUN_ACCESS_KEY = env('MAILGUN_ACCESS_KEY')
MAILGUN_SERVER_NAME = env('MAILGUN_SERVER_NAME')

# Security
CSRF_COOKIE_PATH = '/'
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = env('CSRF_COOKIE_SECURE')
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = env('SESSION_COOKIE_SECURE')
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# i18n
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Oslo'
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
            'filename': 'log/error.log',
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
OIDC_RP_CLIENT_ID = env('OIDC_RP_CLIENT_ID')
OIDC_RP_CLIENT_SECRET = env('OIDC_RP_CLIENT_SECRET')
OIDC_OP_AUTHORIZATION_ENDPOINT = env('OIDC_OP_AUTHORIZATION_ENDPOINT')
OIDC_OP_TOKEN_ENDPOINT = env('OIDC_OP_TOKEN_ENDPOINT')
OIDC_OP_USER_ENDPOINT = env('OIDC_OP_USER_ENDPOINT')
OIDC_RP_SIGN_ALGO = env('OIDC_RP_SIGN_ALGO')
OIDC_OP_JWKS_ENDPOINT = env('OIDC_OP_JWKS_ENDPOINT')

# DRF
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'mozilla_django_oidc.contrib.drf.OIDCAuthentication',
    ]
}

# Swagger
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'oauth': {
            'type': 'oauth2',
            'flow': 'accessCode',
            'authorizationUrl': env('OIDC_OP_AUTHORIZATION_ENDPOINT'),
            'tokenUrl': env('OIDC_OP_TOKEN_ENDPOINT'),
        }
    },
    'USE_SESSION_AUTH': False,
}
