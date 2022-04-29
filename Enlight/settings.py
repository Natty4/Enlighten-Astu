"""
Django settings for Enlight project.
BY : Natnael(MrPGuy)
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = str(os.getenv('DJ_SECRET_KEY'))
CLOUD_NAME_X = str(os.getenv('CLOUD_NAME_X'))
API_KEY_X = str(os.getenv('API_KEY_X'))
API_SECRET_X = str(os.getenv('API_SECRET_X'))

DEBUG = True
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    'django.contrib.sites',


    # 3rd party

    'rest_framework',
    'rest_framework.authtoken',

    'allauth',
    'allauth.account',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth.socialaccount',
    'corsheaders',


    # Local

    'users.apps.UsersConfig',
    'repository.apps.RepositoryConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',    
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Enlight.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'Enlight.wsgi.application'


# Database

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# db_from_env = dj_database_url.config(conn_max_age=500)
# DATABASES['default'].update(db_from_env)



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DBNAME'],
        'HOST': os.environ['DBHOST'],
        'USER': os.environ['DBUSER'],
        'PASSWORD': os.environ['DBPASS'] 
    }
}
# Password validation

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




AUTH_USER_MODEL = 'users.User'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ],
}
REST_AUTH_REGISTER_SERIALIZERS = {
    
    'REGISTER_SERIALIZER': 'users.serializers.UserRegistrationSerializer',
}

AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]



# ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
LOGIN_URL = '/api/auth/login'


ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400 # 1 day in seconds
ACCOUNT_LOGOUT_REDIRECT_URL ='/api/auth/login/'
LOGIN_REDIRECT_URL = '/api/auth/profile'
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/'


REST_USE_JWT = True
JWT_AUTH_COOKIE = 'enlight-web'
SITE_ID = 1

CORS_ALLOW_ALL_ORIGINS = True


# Local (console)EmailBackend

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# SMPT EmailBackend

# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'test@gmail.com'
# EMAIL_HOST_PASSWORD = 'test'
# DEFAULT_FROM_EMAIL = 'test@gmail.com'
# DEFAULT_TO_EMAIL = EMAIL_HOST_USER


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': CLOUD_NAME_X, 
    'API_KEY': API_KEY_X, 
    'API_SECRET': API_SECRET_X,
    # 'EXCLUDE_DELETE_ORPHANED_MEDIA_PATHS': (BASE_DIR / 'media/', BASE_DIR / 'deleted/' ),
}


STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = BASE_DIR / 'static/' 

# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media/'
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
