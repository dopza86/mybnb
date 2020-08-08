"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

import dj_database_url

from django.conf import settings

from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "YqTfR'V%m-s'%2L)]ff}aq#Z~&>4Djn22NV;%,3Mj<@qZ^yd%S"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com']

# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]  # 사용의 편의를 위해 장고 제공앱과 프로젝트 앱으로 나눠버림

THIRD_PARTY_APPS = [
    "django_countries",
]

PROJECT_APPS = [
    "core.apps.CoreConfig",
    "users.apps.UsersConfig",
    "rooms.apps.RoomsConfig",
    "reviews.apps.ReviewsConfig",
    "reservations.apps.ReservationsConfig",
    "lists.apps.ListsConfig",
    "conversations.apps.ConversationsConfig",
]  # 기존에 models.Model을 상속 받아 사용할때는 그냥 users를 사용했으나 AbstracrtUser를 상속받아 사용하니까
# users.apps.UsersConfig 를 사용하며 AUTH_USER_MODEL = "users.User" 를 통해 모델을 참조할수 있다

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    # 미들웨어를 설치해야 세션을 가져와서 번역을 실행한다
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if DEBUG is False:

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
else:

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "HOST": os.environ.get("RDS_HOST"),
            "NAME": os.environ.get("RDS_NAME"),
            "USER": os.environ.get("RDS_USER"),
            "PASSWORD": os.environ.get("RDS_PASSWORD"),
            "PORT": "5432",
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

AUTH_USER_MODEL = "users.User"  # 장고 유저 모델이 기본값이 아니라 유저모델에 오버라이딩한 users.User 을 유저모델 기본값으로 사용

# Some kinds of projects may have authentication requirements for which Django’s built-in User model
# is not always appropriate. For instance, on some sites it makes more sense to use an email address
# as your identification token instead of a username.
# Django allows you to override the default user model by providing a value for the AUTH_USER_MODEL setting
# that references a custom model:
# AUTH_USER_MODEL = 'myapp.MyUser'
# This dotted pair describes the name of the Django app (which must be in your INSTALLED_APPS),
# and the name of the Django model that you wish to use as your user model.

# 일부 종류의 프로젝트에는 Django의 내장 User모델이 항상 적합하지 않은 인증 요구 사항이있을 수 있습니다 .
# 예를 들어, 일부 사이트에서는 사용자 이름 대신 전자 메일 주소를 식별 토큰으로 사용하는 것이 더 합리적입니다.
# Django를 사용하면 사용자 AUTH_USER_MODEL지정 모델을 참조하는 설정 값을 제공하여
# 기본 사용자 모델을 재정의 할 수 있습니다 .

# AUTH_USER_MODEL = 'myapp.MyUser'
# 이 점선 쌍은 Django 앱의 이름 (이어야 함 INSTALLED_APPS)과 사용자 모델로 사용하려는 Django 모델의 이름을 설명합니다.

MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")
# 파일이 저장될 경로를 설정
MEDIA_URL = "/media/"

# 이메일 설정

EMAIL_HOST = "smtp.mailgun.org"
EMAIL_PORT = "25"

EMAIL_HOST_USER = os.environ.get("MAILGUN_USERNAME")
EMAIL_HOST_PASSWORD = os.environ.get("MAILGUN_PASSWORD")

EMAIL_FROM = "noreply@sandbox1eef570fd7ee4a9ca110f0f2fad9115e.mailgun.org"

# Auth

LOGIN_URL = "/users/login/"

# Locale

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"), )
LANGUAGES = [
    ("en", _("English")),
    ("ko", _("Korean")),
    ("cn", _("Chinese")),
]

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)