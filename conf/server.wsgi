
import os
import sys

sys.stdout = sys.stderr

sys.path.append('/srv/billometer/billometer')

import site

site.addsitedir('/srv/billometer/lib/python2.7/site-packages')

# Avoid ``[Errno 13] Permission denied: '/var/www/.python-eggs'`` messages

import os
#os.environ['PYTHON_EGG_CACHE'] = '/www/lostquery.com/mod_wsgi/egg-cache'

sys.path.append('/srv/billometer/billometer')
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
