from .base import *

DEBUG = env('DEBUG')
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': env.db()
}

STUDLAN_FROM_MAIL = env('STUDLAN_FROM_MAIL')
SUPPORT_MAIL = env('SUPPORT_MAIL')

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # real
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # prints

SITE_NAME = env('SITE_NAME')

# Enable and set to your domain when deployed
# CSRF_COOKIE_DOMAIN = 'studlan.no'
CSRF_COOKIE_HTTPONLY = True


