from .base import * 

# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "localhost.com", "*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = env('SITE_ID')

SOCIALACCOUNT_PROVIDERS = {
    'telegram': {
        'TOKEN': env('TG_TOKEN'),
    }
}