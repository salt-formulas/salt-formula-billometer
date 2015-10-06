#!/usr/bin/env python

{%- from "billometer/map.jinja" import server with context %}

import sys
import os
from os.path import join, dirname, abspath, normpath

path = '/srv/billometer'
sys.path.append(join(path, 'lib', 'python{{ server.python_version }}', 'site-packages'))
sys.path.append(join(path, 'billometer'))
sys.path.append(join(path, 'site'))

from django.core.management import execute_from_command_line

import django

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'billometer.settings'
    django.setup()
    execute_from_command_line(sys.argv)
