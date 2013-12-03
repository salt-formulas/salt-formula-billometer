# -*- coding: utf-8 -*-
{%- set app = pillar.billometer.server %}

from os.path import join, dirname, abspath, normpath

DATABASES = {
    'default': {
        {%- if app.database.engine == 'mysql' %}
        'ENGINE': 'django.db.backends.mysql',
        'PORT': '3306',
        'OPTIONS': { 'init_command': 'SET storage_engine=INNODB,character_set_connection=utf8,collation_connection=utf8_unicode_ci', },
        {% else %}
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'PORT': '5432',
        {%- endif %}
        'HOST': '{{ app.database.host }}',
        'NAME': '{{ app.database.name }}',
        'PASSWORD': '{{ app.database.password }}',
        'USER': '{{ app.database.user }}'
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '{{ app.cache.host }}:11211',
        'TIMEOUT': 120,
        'KEY_PREFIX': '{{ app.cache.prefix }}'
    }
}

KEYSTONE_REGION = "{{ app.identity.region }}"
KEYSTONE_SERVICE_TOKEN = "{{ app.identity.token }}"
KEYSTONE_SERVICE_ENDPOINT="http://{{ app.identity.host }}:{{ app.identity.port }}/v{{ app.identity.api_version }}.0"

OPENSTACK_KEYSTONE_URL = KEYSTONE_SERVICE_ENDPOINT

EMAIL_HOST = '{{ app.mail.host }}',
EMAIL_HOST_USER = '{{ app.mail.user }}',
EMAIL_HOST_PASSWORD = '{{ app.mail.password }}'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Admin', 'mail@newt.cz'),
)

MANAGERS = ADMINS

SITE_ID = 1
SITE_NAME = 'billometer'

TIME_ZONE = '{{ pillar.system.timezone }}'

LANGUAGE_CODE = 'en'

LANGUAGES = (
#    ('cs', 'CS'),
    ('en', 'EN'),
)

USE_I18N = True

MEDIA_ROOT = '/srv/billometer/media/'
MEDIA_URL = '/media/'
STATIC_ROOT = '/srv/billometer/static/'
STATIC_URL = '/static/'

SECRET_KEY = '{{ app.secret_key }}'

ADMIN_MEDIA_PREFIX = '/static/admin/'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'billometer.urls'

TEMPLATE_DIRS = (
)

INSTALLED_APPS = (
    'billometer',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.staticfiles',
    'south',
    'rest_framework',
    'openstack_auth',
)

STATICFILES_FINDERS =(
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'keystone_auth.backend.KeystoneBackend',
)

REST_FRAMEWORK = {
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
