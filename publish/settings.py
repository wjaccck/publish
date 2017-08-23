#coding=utf-8
"""
Django settings for publish project.

Generated by 'django-admin startproject' using Django 1.8.17.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vpe4p=h+2kfh^ah48w7m6qnd4)b9j8-)6++*5ce4z@u_!clcfp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
PYTHONOPTIMIZE = 1

ALLOWED_HOSTS = ['127.0.0.1','publish.eju-inc.com']
WHITE_IPS=['10.0.8.0/24','10.106.0.0/24','10.192.0.0/16']
INTERNAL_IPS=['10.192.0.0/16','172.29.28.126']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_extensions',
    'api',
    'django_select2',
    'webui',
    'bootstrap_pagination',
    'corsheaders',
    'rest_framework_swagger',
    'debug_toolbar',
    'djcelery',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


## debug tool config

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

#debug host


#swagger

SWAGGER_SETTINGS = {
    'LOGIN_URL': 'rest_framework:login',
    'LOGOUT_URL': 'rest_framework:logout',
    'USE_SESSION_AUTH': True,
    'DOC_EXPANSION': 'list',
    'APIS_SORTER': 'alpha'
}


ROOT_URLCONF = 'publish.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'publish.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db2.sqlite3'),
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'publish',
        'USER': 'publishadmin',
        'PASSWORD': 'Eju@publish1',
        'HOST': '10.120.180.40',
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'core.pagination.DefaultResultsSetPagination',
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_filters.backends.DjangoFilterBackend',
    ),
}

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static').replace('/','\\\\')
STATICFILES_DIRS = (
    # os.path.join(BASE_DIR, "static").replace('/','\\\\'),
    # 'c:\\work\\open\\publish\\static',
    # 'd:\\work\\publish\\static',
    '/opt/app/publish/static',
)

import djcelery
# from kombu import Exchange, Queue
djcelery.setup_loader()
# Celery Settings
BROKER_URL = 'redis://:cc62601845fc3c66cdbb81915a871605@127.0.0.1:6379/9'
CELERY_RESULT_BACKEND = 'redis://:cc62601845fc3c66cdbb81915a871605@127.0.0.1:6379/10'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
# CELERY_QUEUES = (
#     Queue('10.99.70.27'),
#     Queue('10.99.70.33'),
#     Queue('for_task_B', Exchange('for_task_B'), routing_key='for_task_B'),
# )

CORS_ORIGIN_ALLOW_ALL = True

# LOG_PATH = '/opt/app/ips/act.log'
LOG_PATH = os.path.join(BASE_DIR, 'act.log')
LOG_CMD_PATH = os.path.join(BASE_DIR, 'cmd.log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s %(module)s.%(funcName)s-[%(lineno)d] %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'standard',
        },
        'windows_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_PATH,
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'act_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_CMD_PATH,
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'windows_handler'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['windows_handler'],
            'level': 'INFO',
            'propagate': False
        },
        'webapp': {
            'handlers': ['windows_handler'],
            'level': 'INFO',
            'propagate': False
        },
        'publish': {
            'handlers': ['act_handler'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}

# Debug Toolbar
# DEBUG_TOOLBAR_CONFIG = {
#     'JQUERY_URL': '//apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js',
# }

LOGIN_REDIRECT_URL='/'
LOGIN_URL='/login/'
LOGOUT_REDIRECT_URL='/login/'





# AUTH_LDAP_SERVER_URI = "ldap://172.28.100.101:389"
# AUTH_LDAP_BIND_DN = unicode("CN=admin_cy,OU=创研中心,DC=shfang,DC=net","utf8")
# AUTH_LDAP_BIND_PASSWORD = "Ehouse027="
# OU=unicode('OU=创研中心,DC=shfang,DC=net', 'utf8')
# AUTH_LDAP_USER_SEARCH = LDAPSearch(OU, ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)")
#
# AUTH_LDAP_USER_ATTR_MAP = {
#        "first_name": "givenName",
#        "last_name": "sn",
#        "email":"mail"
# }
#
# AUTHENTICATION_BACKENDS = (
#     'django_auth_ldap.backend.LDAPBackend',
#     'django.contrib.auth.backends.ModelBackend',
# )


# Select 2
AUTO_RENDER_SELECT2_STATICS = True
SELECT2_BOOTSTRAP = True
# Set the cache backend to select2
SELECT2_CACHE_BACKEND = 'select2'
REDIS_TIMEOUT=7*24*60*60
CUBES_REDIS_TIMEOUT=60*60
NEVER_REDIS_TIMEOUT=365*24*60*60
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:cc62601845fc3c66cdbb81915a871605@127.0.0.1:6379/11",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    'select2': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:cc62601845fc3c66cdbb81915a871605@127.0.0.1:6379/12",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '//apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js',
}