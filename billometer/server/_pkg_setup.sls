{%- from "billometer/map.jinja" import server with context %}

billometer_debconf:
  debconf.set:
  - name: billometer
  - data:
      'billometer/user':
        type: string
        value: {{ server.user }}
      'billometer/group':
        type: string
        value: {{ server.group }}
      'billometer/bind_host':
        type: string
        value: {{ server.bind.address }}
      'billometer/bind_port':
        type: string
        value: {{ server.bind.port }}
      'billometer/workers':
        type: string
        value: '{{ server.get('workers', grains.num_cpus * 2 + 1) }}'
      'billometer/log_level':
        type: string
        value: {{ server.log_level }}

billometer_packages:
  pkg.installed:
  - names: {{ server.pkgs }}
  - require:
    - debconf: billometer_debconf
  - require_in:
    - file: django_conf_settings
    - file: django_conf_celery
    - cmd: django_migrate_database
    - file: {{ server.dir.base }}/bin/celery_config.py

{{ server.dir.base }}/bin/celery_config.py:
  file.symlink:
    - target: /etc/billometer/celery.py