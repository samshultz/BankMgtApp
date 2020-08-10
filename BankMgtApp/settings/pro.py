from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bankapp',
	'USER': 'samshultz',
	'PASSWORD': 'reductionism',
	'HOST': 'localhost',
	'PORT': '',
    }
}

EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'taiwogabrielsamuel@gmail.com'
EMAIL_HOST_PASSWORD = 'mcwptkjuzwqrmivn'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'