{%- if pillar.billometer.server.enabled %}

include:
- git
- python

billometer_packages:
  pkg.installed:
  - names:
    - python-pip
    - python-virtualenv
    - python-memcache
    - python-psycopg2
    - python-imaging
    - python-docutils
    - python-simplejson
    - python-tz
    - python-pygraphviz
    - python-dev
    - gettext
    - libpq-dev
  - require:
    - pkg: python_packages

/srv/billometer:
  virtualenv.manage:
  - system_site_packages: True
  - requirements: salt://billometer/conf/requirements.txt
  - require:
    - pkg: billometer_packages

{{ pillar.billometer.server.source.address }}:
  git.latest:
  - target: /srv/billometer/billometer
  - rev: {{ pillar.billometer.server.source.rev }}
  - require:
    - virtualenv: /srv/billometer
    - pkg: git_packages

/srv/billometer/server.wsgi:
  file:
  - managed
  - source: salt://billometer/conf/server.wsgi
  - mode: 755
  - template: jinja
  - require:
    - virtualenv: /srv/billometer

/srv/billometer/site/core:
  file:
  - directory
  - user: root
  - group: root
  - mode: 755
  - makedirs: true
  - require:
    - virtualenv: /srv/billometer

/srv/billometer/media:
  file:
  - directory
  - user: www-data
  - group: www-data
  - mode: 755
  - makedirs: true
  - require:
    - virtualenv: /srv/billometer

/srv/billometer/static:
  file:
  - directory
  - user: root
  - group: root
  - mode: 755
  - makedirs: true
  - require:
    - virtualenv: /srv/billometer

/srv/billometer/logs:
  file:
  - directory
  - user: www-data
  - group: www-data
  - mode: 755
  - makedirs: true
  - require:
    - virtualenv: /srv/billometer

/srv/billometer/site/core/settings.py:
  file:
  - managed
  - user: root
  - group: root
  - source: salt://billometer/conf/settings.py
  - template: jinja
  - mode: 644
  - require:
    - file: /srv/billometer/site/core

/srv/billometer/site/core/__init__.py:
  file:
  - managed
  - user: root
  - group: root
  - template: jinja
  - mode: 644
  - require:
    - file: /srv/billometer/site/core

/srv/billometer/site/manage.py:
  file:
  - managed
  - user: root
  - group: root
  - source: salt://billometer/conf/manage.py
  - template: jinja
  - mode: 755
  - require:
    - file: /srv/billometer/site/core

sync_database_billometer:
  cmd.run:
  - name: python manage.py syncdb --noinput
  - cwd: /srv/billometer/site
  - require:
    - file: /srv/billometer/site/manage.py

migrate_database_billometer:
  cmd.run:
  - name: python manage.py migrate --noinput
  - cwd: /srv/billometer/site
  - require:
    - cmd: sync_database_billometer

collect_static_billometer:
  cmd.run:
  - name: python manage.py collectstatic --noinput
  - cwd: /srv/billometer/site
  - require:
    - cmd: sync_database_billometer

{%- endif %}