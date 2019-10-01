import os
import environ
import raven
from corsheaders.defaults import default_headers

from modules.achievements.events_manager import EventsManager

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = environ.Path(__file__) - 2
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(str,),
    BUNDLE_DIR=str,
    STATS_FILE=str,
)

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')



INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
] + [
    'raven.contrib.django.raven_compat',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'suit_redactor',
    'suit_ckeditor',
    "sortedm2m",
    'django_extensions',
    'polymorphic',
    'django.contrib.contenttypes',
] + [
    'users',
    'tasks',
    'resources',
    'modules.order_strategy',
    'modules.agreement',
    'modules.aggregation',
    'modules.packages',
    'modules.feedback',
    'modules.validators',
    'modules.bounty',
    'modules.statistics',
    'modules.achievements',
    'modules.sender'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'funcrowd.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'funcrowd/templates')],
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

WSGI_APPLICATION = 'funcrowd.wsgi.application'

DATABASES = {
    'default': env.db(),
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.NumericPasswordValidator',
    },
]


AUTH_USER_MODEL = 'users.EndWorker'
SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = 'none'


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
]

NOTEBOOK_ARGUMENTS = [
    '--ip', '0.0.0.0',
    '--port', '8080',
    '--notebook-dir', 'notebooks',
    '--allow-root'
]


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

CORS_ALLOW_HEADERS = default_headers + (
    'cache-control',
    'x-requested-with',
    'content-disposition',
    'handle-errors-generically',
    'authorization',
    'backendauth'
)

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL=True


RAVEN_CONFIG = {}
if 'SENTRY_DNS' in env:
    RAVEN_CONFIG = {
        'dsn': env('SENTRY_DNS'),
    }


# File storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', '')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_QUERYSTRING_AUTH = False


# Sendgrid
SENDGRID_API_KEY = env("SENDGRID_API_KEY")
SENDGRID_USERNAME = env("SENDGRID_USERNAME")
SENDGRID_PASSWORD = env("SENDGRID_PASSWORD")


events_manager = EventsManager()
