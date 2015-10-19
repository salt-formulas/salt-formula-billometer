{%- from "billometer/map.jinja" import server with context %}
{%- if server.enabled %}

include:
- git
- python

billometer_packages:
  pkg.installed:
  - names: {{ server.pkgs }}
  - require:
    - pkg: python_packages

/srv/billometer:
  virtualenv.manage:
  - system_site_packages: True
  - requirements: salt://billometer/files/requirements.txt
  - require:
    - pkg: billometer_packages

billometer_user:
  user.present:
  - name: billometer
  - system: True
  - home: /srv/billometer
  - require:
    - virtualenv: /srv/billometer

{{ server.source.address }}:
  git.latest:
  - target: /srv/billometer/billometer
  - rev: {{ server.source.rev }}
  - require:
    - virtualenv: /srv/billometer
    - pkg: git_packages

/srv/billometer/site/wsgi.py:
  file.managed:
  - source: salt://billometer/files/wsgi.py
  - mode: 755
  - template: jinja
  - require:
    - file: /srv/billometer/site

/srv/billometer/bin/gunicorn_start.sh:
  file.managed:
  - source: salt://billometer/files/gunicorn_start
  - mode: 700
  - user: billometer
  - group: billometer
  - template: jinja
  - require:
    - virtualenv: /srv/billometer

billometer_dirs:
  file.directory:
  - names:
    - /etc/billometer
    - /srv/billometer/site
    - /srv/billometer/static
    - /srv/billometer/logs
  - user: billometer
  - group: billometer
  - mode: 755
  - makedirs: true
  - require:
    - virtualenv: /srv/billometer

/srv/billometer/media:
  file.directory:
  - user: billometer
  - group: billometer
  - mode: 755
  - makedirs: true
  - require:
    - virtualenv: /srv/billometer

/etc/billometer/settings.py:
  file.managed:
  - user: root
  - group: root
  - source: salt://billometer/files/settings.py
  - template: jinja
  - mode: 644
  - require:
    - file: billometer_dirs

/srv/billometer/site/celery_config.py:
  file.managed:
  - user: root
  - group: root
  - source: salt://billometer/files/celery.py
  - template: jinja
  - mode: 755
  - require:
    - file: billometer_dirs

/srv/billometer/site/manage.py:
  file.managed:
  - user: root
  - group: root
  - source: salt://billometer/files/manage.py
  - template: jinja
  - mode: 755
  - require:
    - file: billometer_dirs

/srv/billometer/logs/collector.log:
  file.managed:
  - user: billometer
  - group: billometer
  - mode: 777
  - require:
    - file: billometer_dirs

/srv/billometer/logs/billometer.log:
  file.managed:
  - user: billometer
  - group: billometer
  - mode: 777
  - require:
    - file: billometer_dirs

migrate_database_billometer:
  cmd.run:
  - name: source /srv/billometer/bin/activate; python manage.py migrate --noinput
  - cwd: /srv/billometer/site
  - require:
    - file: /srv/billometer/site/manage.py

collect_static_billometer:
  cmd.run:
  - name: source /srv/billometer/bin/activate; python manage.py collectstatic --noinput
  - cwd: /srv/billometer/site
  - require:
    - cmd: migrate_database_billometer

{%- endif %}