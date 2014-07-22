# -*- coding: utf-8 -*-
{%- from "billometer/map.jinja" import server with context %}

from os.path import join, dirname, abspath, normpath

DATABASES = {
    'default': {
        {%- if server.database.engine == 'mysql' %}
        'ENGINE': 'django.db.backends.mysql',
        'PORT': '3306',
        'OPTIONS': { 'init_command': 'SET storage_engine=INNODB,character_set_connection=utf8,collation_connection=utf8_unicode_ci', },
        {% else %}
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'PORT': '5432',
        {%- endif %}
        'HOST': '{{ server.database.host }}',
        'NAME': '{{ server.database.name }}',
        'PASSWORD': '{{ server.database.password }}',
        'USER': '{{ server.database.user }}'
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '{{ server.cache.host }}:11211',
        'TIMEOUT': 120,
        'KEY_PREFIX': '{{ server.cache.prefix }}'
    }
}

KEYSTONE_REGION = "{{ server.identity.get('region', 'RegionOne') }}"
{% if server.identity.token is defined %}
KEYSTONE_SERVICE_TOKEN = "{{ server.identity.token }}"
{% endif %}
{% if server.identity.user is defined %}
KEYSTONE_USER = "{{ server.identity.user }}"
{% endif %}
{% if server.identity.password is defined %}
KEYSTONE_PASSWORD = "{{ server.identity.password }}"
{% endif %}
KEYSTONE_SERVICE_ENDPOINT="http://{{ server.identity.host }}:{{ server.identity.port }}/v2.0"

OPENSTACK_KEYSTONE_URL = KEYSTONE_SERVICE_ENDPOINT

OPENSTACK_SSL_NO_VERIFY = True

OPENSTACK_API_VERSIONS = {
    'identity': 2.0
}

USE_TZ = True

OPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT = False
OPENSTACK_KEYSTONE_DEFAULT_DOMAIN = 'Default'

#AVAILABLE_REGIONS = [
#    (OPENSTACK_KEYSTONE_URL, 'Default region'),
#]

EMAIL_HOST = '{{ server.mail.host }}',
EMAIL_HOST_USER = '{{ server.mail.user }}',
EMAIL_HOST_PASSWORD = '{{ server.mail.password }}'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Admin', 'mail@newt.cz'),
)

MANAGERS = ADMINS

SITE_ID = 1
SITE_NAME = 'billometer'

TIME_ZONE = 'Europe/Prague'
{#
TIME_ZONE = '{{ pillar.system.timezone }}'
#}

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

SECRET_KEY = '{{ server.secret_key }}'

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
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'billometer.urls'

TEMPLATE_DIRS = (
)

INSTALLED_APPS = (
    'django',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.staticfiles',
    'south',
    'rest_framework',
    'openstack_auth',
#    'djcelery',
    'billometer',
)

STATICFILES_FINDERS =(
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/admin/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'openstack_auth.backend.KeystoneBackend',
)

REST_FRAMEWORK = {
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
