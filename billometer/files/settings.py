# -*- coding: utf-8 -*-
{%- from "billometer/map.jinja" import server with context %}

from os.path import join, dirname, abspath, normpath

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        {%- if server.database.engine == 'mysql' %}
        'ENGINE': 'django.db.backends.mysql',
        'PORT': '3306',
        'OPTIONS': {'init_command': 'SET storage_engine=INNODB,character_set_connection=utf8,collation_connection=utf8_unicode_ci', },
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

BROKER_URL = 'amqp://{{ server.message_queue.user }}:{{ server.message_queue.password }}@{{ server.message_queue.host }}:{{ server.message_queue.get("port",5672) }}/{{ server.message_queue.virtual_host }}'

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
KEYSTONE_SERVICE_ENDPOINT = "http://{{ server.identity.host }}:{{ server.identity.port }}/v2.0"

OPENSTACK_KEYSTONE_URL = KEYSTONE_SERVICE_ENDPOINT

OPENSTACK_SSL_NO_VERIFY = True

OPENSTACK_API_VERSIONS = {
    'identity': 2.0
}

USE_TZ = True

OPENSTACK_KEYSTONE_MULTIDOMAIN_SUPPORT = False
OPENSTACK_KEYSTONE_DEFAULT_DOMAIN = 'Default'


{% if server.mail.engine == 'console' %}
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
{% else %}
EMAIL_HOST = '{{ server.mail.host }}',
EMAIL_HOST_USER = '{{ server.mail.user }}',
EMAIL_HOST_PASSWORD = '{{ server.mail.password }}'
{% endif %}

DEBUG = False
TEMPLATE_DEBUG = DEBUG

MEDIA_ROOT = '/srv/billometer/media/'
STATIC_ROOT = '/srv/billometer/static/'

TIME_ZONE = 'Europe/Prague'

{%- if pillar.linux is defined %}
TIME_ZONE = '{{ pillar.linux.system.timezone }}'
{%- else %}
TIME_ZONE = '{{ pillar.system.timezone }}'
{%- endif %}

SECRET_KEY = '{{ server.secret_key }}'

{% if server.logging is defined %}
LOCAL_INSTALLED_APPS = (
    'raven.contrib.django.raven_compat',
)
{% endif %}

{% if server.resource_price is defined %}
RESOURCE_PRICE = {{server.get("resource_price", {}) | python}}
{% else %}
RESOURCE_PRICE = {
    'cinder.volume': {
        '7k2_SAS': '0.008205',
        '10k_SAS': '0.027383',
        '15k_SAS': '0.034232',
        'EasyTier': '0.041082',
    },
    'nova.memory': '0.000369',
    'nova.cpu': '0.821904',
    'neutron.floating_ip': '0.136972',
    'glance.image': '0.002739',
}
{% endif %}

SYNC_TIME = {{server.get("sync_time", 60)}}
COLLECT_TIME = {{server.get("collect_time", 120)}}

{%- if server.metric is defined %}

{%- if server.metric.get("in", {"engine": ""}).engine == 'graphite' %}
GRAPHITE_HOST = "{{ server.metric.in.host }}"
GRAPHITE_PORT = "{{ server.metric.in.port }}"
GRAPHITE_ENDPOINT = 'http://%s:%s' % (GRAPHITE_HOST, GRAPHITE_PORT)
{%- endif %}

{%- if server.metric.get("out", {"engine": ""}).engine == 'statsd' %}
STATSD_HOST = "{{ server.metric.out.host }}"
STATSD_PORT = "{{ server.metric.out.get('port', 8125) }}"
STATSD_PREFIX = "{{ server.metric.out.get('prefix', '') }}"
{%- endif %}

{%- if server.metric.get("out", {"engine": ""}).engine == 'carbon' %}
CARBON_HOST = "{{ server.metric.out.host }}"
CARBON_PORT = "{{ server.metric.out.get('port', 2003) }}"
{%- endif %}

{%- endif %}

RAVEN_CONFIG = {
{% if server.logging is defined %}
    'dsn': '{{ server.logging.dsn }}',
{% endif %}
}
{% if server.logging is defined %}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/srv/billometer/logs/billometer.log',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    }
}
{% endif %}

BILLING_CONFIG = {{server.get("billing_config", {}) | python}}

BILLING_EXTRA_RESOURCES = {{server.get("extra_resource", {}) | python}}
