# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
                'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG', # change debug level as appropiate
            'propagate': False,
        },
    },
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'project',
#         'USER': 'projectuser',
#         'PASSWORD': 'password',
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'test1',
#         'USER': 'projectuser',
#         'PASSWORD': 'password',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }




####################베타 테스트 데이터 베이스
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'phopo_close_beta',
#         'USER': 'projectuser',
#         'PASSWORD': 'password',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }
################클로즈 베타 테스트 테스트2
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'phopo_cbt_second',
#         'USER': 'projectuser',
#         'PASSWORD': 'password',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

####################베타 테스트 데이터 베이스 2
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'test2',
#         'USER': 'projectuser',
#         'PASSWORD': 'password',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }




# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DJANGO_DB_NAME', 'test1'),
#         'USER': os.environ.get('DJANGO_DB_USERNAME', 'projectuser'),
#         'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD', 'password'),
#         'HOST': os.environ.get('DJANGO_DB_HOST', 'localhost'),
#         'PORT': os.environ.get('DJANGO_DB_PORT', '5432'),
#     }
# }
