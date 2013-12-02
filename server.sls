{%- if pillar.billometer.server.enabled %}
 
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

/srv/billometer/billometer:
  file:
  - directory
  - require:
    - virtualenv: /srv/billometer

/srv/billometer/billometer/billometer:
  file:
  - directory
  - user: www-data
  - group: www-data
  require:
  - file: /srv/billometer/billometer

/srv/billometer/billometer/server.wsgi:
  file:
  - managed
  {%- if pillar.system.environment == 'prod' %}
  - user: root
  - group: root
  {% endif %}
  - source: salt://billometer/conf/server.wsgi
  - mode: 755
  - template: jinja
  - require:
    - file: /srv/billometer/billometer

/srv/billometer/media:
  file:
  - directory
  {%- if pillar.system.environment == 'prod' %}
  - user: www-data
  - group: www-data
  {% endif %}
  - mode: 755
  - makedirs: true
  - require:
    - file: /srv/billometer/billometer

/srv/billometer/static:
  file:
  - directory
  {%- if pillar.system.environment == 'prod' %}
  - user: root
  - group: root
  {% endif %}
  - mode: 755
  - makedirs: true
  - require:
    - file: /srv/billometer/billometer

/srv/billometer/logs:
  file:
  - directory
  - user: www-data
  - group: www-data
  - mode: 755
  - makedirs: true
  - require:
    - file: /srv/billometer/billometer

/srv/billometer/billometer/settings.py:
  file:
  - managed
  {%- if pillar.system.environment == 'prod' %}
  - user: root
  - group: root
  {% endif %}
  - source: salt://billometer/conf/settings.py
  - template: jinja
  - mode: 644
  - require:
    - file: /srv/billometer/billometer

/srv/billometer/billometer/manage.py:
  file:
  - managed
  {%- if pillar.system.environment == 'prod' %}
  - user: root
  - group: root
  {% endif %}
  - source: salt://billometer/conf/manage.py
  - template: jinja
  - mode: 755
  - require:
    - file: /srv/billometer/billometer/settings.py

sync_database_billometer:
  cmd.run:
  - name: python manage.py syncdb --noinput
  - cwd: /srv/billometer/billometer
  - require:
    - file: /srv/billometer/billometer/manage.py

migrate_database_billometer:
  cmd.run:
  - name: python manage.py migrate --noinput
  - cwd: /srv/billometer/billometer
  - require:
    - cmd: sync_database_billometer

collect_static_billometer:
  cmd.run:
  - name: python manage.py collectstatic --noinput
  - cwd: /srv/billometer/billometer
  - require:
    - cmd: sync_database_billometer

{%- endif %}