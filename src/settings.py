import environ

base_dir = environ.Path(__file__) - 2
src_dir = environ.Path(__file__) - 1
env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(base_dir("env"))

INSTALLED_APPS = [
    # Local
    # "apps.competition",
    "apps.event",
    "apps.article",
    # "apps.payment",
    # "apps.seating",
    "apps.sponsor",
    # "apps.team",
    "apps.user",

    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "rest_framework_swagger",
    "mozilla_django_oidc",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "mozilla_django_oidc.middleware.SessionRefresh",
]

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "auth.backends.OidcAuthBackend",
)

# Basics
BASE_DIR = base_dir
DEBUG = env("DEBUG")
TEMPLATE_DEBUG = DEBUG
SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")
SITE_NAME = env("SITE_NAME")
WSGI_APPLICATION = "wsgi.application"
ROOT_URLCONF = "urls"
AUTH_USER_MODEL = "user.User"
LOGIN_URL = "/auth/login"
LOGIN_REDIRECT_URL = "/"
LOGIN_REDIRECT_URL_FAILURE = "/"
LOGOUT_REDIRECT_URL = "/"

# Database
DATABASES = {
    "default": env.db("DATABASE_URL"),
}

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [src_dir("templates")],
        "APP_DIRS": True,
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

# Email
DEFAULT_MAIL = env("DEFAULT_MAIL", default="app@localhost")
SUPPORT_MAIL = env("SUPPORT_MAIL", default="support@localhost")
EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
# Mailgun
MAILGUN_ACCESS_KEY = env("MAILGUN_ACCESS_KEY", default="")
MAILGUN_SERVER_NAME = env("MAILGUN_SERVER_NAME", default="")

# Security
CSRF_COOKIE_PATH = "/"
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = env("CSRF_COOKIE_SECURE", default=True)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = env("SESSION_COOKIE_SECURE", default=True)
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = base_dir("static")

# i18n
LANGUAGE_CODE = "en-us"
TIME_ZONE = env("TIME_ZONE", default="UTC")
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "[%(asctime)s] [%(levelname)s] %(message)s",
        },
    },
    "handlers": {
        "error_file": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": base_dir(env("LOG_DIR", default="log"), "error.log"),
            "maxBytes": 5 * 1024 * 1024,  # 5 MB
            "backupCount": 5,
            "formatter": "standard",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["error_file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

# DRF
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "mozilla_django_oidc.contrib.drf.OIDCAuthentication",
        # Keeps the user logged in after OIDC auth
        "rest_framework.authentication.SessionAuthentication",
    ],
}

# OIDC
OIDC_RP_CLIENT_ID = env("OIDC_RP_CLIENT_ID", default="")
OIDC_RP_CLIENT_SECRET = env("OIDC_RP_CLIENT_SECRET", default="")
OIDC_OP_AUTHORIZATION_ENDPOINT = env("OIDC_OP_AUTHORIZATION_ENDPOINT", default="")
OIDC_OP_TOKEN_ENDPOINT = env("OIDC_OP_TOKEN_ENDPOINT", default="")
OIDC_OP_USER_ENDPOINT = env("OIDC_OP_USER_ENDPOINT", default="")
OIDC_RP_SIGN_ALGO = env("OIDC_RP_SIGN_ALGO", default="")
OIDC_OP_JWKS_ENDPOINT = env("OIDC_OP_JWKS_ENDPOINT", default="")
# OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS = 15 * 60

# Swagger
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "oauth": {
            "type": "oauth2",
            "flow": "accessCode",
            "authorizationUrl": env("OIDC_OP_AUTHORIZATION_ENDPOINT", default=""),
            "tokenUrl": env("OIDC_OP_TOKEN_ENDPOINT", default=""),
        },
    },
    "USE_SESSION_AUTH": False,
}
