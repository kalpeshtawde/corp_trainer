# Database
    # https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tosdb',
        'USER': 'tos',
        'PASSWORD': 'ratnagiri',
        'HOST': 'localhost',
        'PORT': '5432',                      # Set to empty string for default.
    }
}
