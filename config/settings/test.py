import environ

from .base import *

env = environ.Env(    
    DEBUG=(bool, False),
    SITE_ID=(int, 1),
    TG_TOKEN=(str, '')
)

env_file = BASE_DIR / ".env"
environ.Env.read_env(env_file= env_file)

# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "localhost.com", "*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    } 
}

# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = env('SITE_ID')

SOCIALACCOUNT_PROVIDERS = {
    'telegram': {
        'TOKEN': env('TG_TOKEN'),
    }
}
