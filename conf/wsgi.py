
import os
import sys

sys.stdout = sys.stderr

import site

site.addsitedir('/srv/billometer/lib/python2.7/site-packages')

import os
#os.environ['PYTHON_EGG_CACHE'] = '/www/lostquery.com/mod_wsgi/egg-cache'

sys.path.append('/srv/billometer/billometer')
sys.path.append('/srv/billometer/site')
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
