{%- from "billometer/map.jinja" import server with context %}
{%- if server.enabled %}

include:
{%- if server.source.engine == 'git' %}
- billometer.server._git_setup
{%- else %}
- billometer.server._pkg_setup

django_conf_settings:
  file.managed:
  - name: /etc/billometer/settings.py
  - user: root
  - group: billometer
  - source: salt://billometer/files/settings.py
  - template: jinja
  - mode: 640

django_conf_celery:
  file.managed:
  - name: /etc/billometer/celery.py
  - user: root
  - group: billometer
  - source: salt://billometer/files/celery.py
  - template: jinja
  - mode: 640

django_migrate_database:
  cmd.run:
  - name: {{ server.dir.base }}/bin/python {{ server.dir.base }}/bin/manage.py migrate --noinput
  - require:
    - file: django_conf_settings
{%- endif %}

{%- endif %}
