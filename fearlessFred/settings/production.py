# -*- coding: utf-8 -*-
from .base import *

DEBUG = env('DEBUG')
TEMPLATE_DEBUG = DEBUG


SECRET_KEY = env('SECRET_KEY')

DATABASES = {
    'default': env.db()
}

STUDLAN_FROM_MAIL = env('STUDLAN_FROM_MAIL')
SUPPORT_MAIL = env('SUPPORT_MAIL')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # real
EMAIL_HOST = "smtp.domain.no"
DEFAULT_FROM_EMAIL = STUDLAN_FROM_MAIL
REGISTER_FROM_MAIL = DEFAULT_FROM_EMAIL
#Port 25
EMAIL_PORT = env('EMAIL_PORT')

SITE_NAME = env('SITE_NAME')
ALLOWED_HOSTS = env('ALLOWED_HOSTS')

#Enable and set to your domain when deployed
CSRF_COOKIE_DOMAIN = 'domain.no'
CSRF_COOKIE_HTTPONLY = True


