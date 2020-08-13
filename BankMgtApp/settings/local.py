from .base import *

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

GEOIP_PATH = r"C:\Users\Samsh\Desktop\Django Projects\BankMgtApp\BankMgtApp\settings\geoipupdate"