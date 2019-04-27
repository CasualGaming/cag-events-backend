from .base import *
DEBUG = env('DEBUG')
TEMPLATE_DEBUG = DEBUG

# TODO fix
#####
DATABASES = {}
useSqlite = env('USE_SQLITE')
if useSqlite:
    DATABASES['default'] = env.db('SQLITE_URL', default='sqlite:////'+os.path.join(BASE_DIR+'db.sqlite3'))
else:
    DATABASES['default'] = env.db()

#DATABASES = {
#    #'default': env.db(),
#}
#####

STUDLAN_FROM_MAIL = env('STUDLAN_FROM_MAIL')
SUPPORT_MAIL = env('SUPPORT_MAIL')

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # real
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # prints

SITE_NAME = env('SITE_NAME')

# Enable and set to your domain when deployed
# CSRF_COOKIE_DOMAIN = 'studlan.no'
CSRF_COOKIE_HTTPONLY = True


