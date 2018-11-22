import os
import environ

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
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
] + [
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'suit_redactor',
    'suit_ckeditor',
    "sortedm2m",
    'django_extensions',
] + [
    'users',
    'tasks',
    'modules.order_strategy',
    'modules.quality_control',
    'modules.packages',
    'modules.feedback'
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

from corsheaders.defaults import default_headers
CORS_ALLOW_HEADERS = default_headers + (
    'cache-control',
    'x-requested-with',
    'content-disposition',
    'handle-errors-generically',
    'authorization',
    'backendauth'
)

"""
CORS_ORIGIN_WHITELIST = (
    u'localhost',
    u'127.0.0.1',
    u'78.8.194.28'
    u'62.181.9.75',
    u'http://www.test-cors.org',
    u'test-cors.org'
)
"""
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL=True
#CORS_ORIGIN_WHITELIST = (u"*", )

