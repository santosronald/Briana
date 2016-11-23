__author__ = 'klaatu'
from .base import *

ALLOWED_HOSTS = ['192.241.247.216', 'www.brianaapp.com', 'brianaapp.com']
DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'briana',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_URL = '/static/'
APPSECRET_PROOF = False
ADMINS = (
    ('Erik Admin', 'erikd.guiba@gmail.com'),
)
