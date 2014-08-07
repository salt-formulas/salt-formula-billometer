{%- from "billometer/map.jinja" import server with context %}
{%- set broker =  server.message_queue %}

import sys
import os

sys.path.append('/srv/billometer/lib/python{{ server.python_version }}/site-packages')
sys.path.append('/srv/billometer/billometer')
sys.path.append('/srv/billometer/site')

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

from datetime import timedelta
from kombu import Queue, Exchange
from celery import Celery
import logging

logger = logging.getLogger("billometer.collector")

BROKER_URL = 'amqp://{{ broker.user }}:{{ broker.password }}@{{ broker.host }}:{{ broker.get('port', '5672') }}/{{ broker.virtual_host }}'

CELERY_IMPORTS = ("billometer.tasks")

CELERY_RESULT_BACKEND = "amqp"
CELERY_RESULT_EXCHANGE = 'results'
CELERY_RESULT_EXCHANGE_TYPE = 'fanout'
CELERY_TASK_RESULT_EXPIRES = 120

default_exchange = Exchange('default', type='fanout')

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml', 'application/x-python-serialize',]

CELERY_REDIRECT_STDOUTS_LEVEL = "INFO"

CELERY_QUEUES = (
	Queue('default', default_exchange, routing_key='default'),
)

CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_DEFAULT_ROUTING_KEY = 'default'

CELERY_TIMEZONE = 'UTC'

CELERYBEAT_SCHEDULE = {
    'sync_keystone': {
        'task': 'billometer.tasks.sync_keystone',
        'schedule': timedelta(seconds={{ server.get("sync_time", 60) }}),
        'args': tuple()
    },
    'sync_nova': {
        'task': 'billometer.tasks.sync_nova',
        'schedule': timedelta(seconds={{ server.get("sync_time", 60) }}),
        'args': tuple()
    },
    'collect_nova': {
        'task': 'billometer.tasks.sync_nova',
        'schedule': timedelta(seconds={{ server.get("collect_time", 120) }}),
        'args': tuple()
    },
}

celery = Celery('collector', broker=BROKER_URL)
