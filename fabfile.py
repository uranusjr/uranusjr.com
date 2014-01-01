#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os.path
from six.moves import configparser
from fabric.api import cd, run
from fabric.decorators import task


try:
    ConfigParser = configparser.SafeConfigParser
except AttributeError:  # Python 3 renames SafeConfigParser to ConfigParser
    ConfigParser = configparser.ConfigParser


def get_uwsgi_config():
    ini_path = os.path.join(os.path.dirname(__file__), 'uwsgi.ini')
    config = ConfigParser()
    config.read(ini_path)
    return config


@task
def deploy():
    config = get_uwsgi_config()
    pid_file_path = config.get('uwsgi', 'pidfile')
    project_dir = '/var/django/dev/uranusjr.com'
    with cd(project_dir):
        run('git reset HEAD --hard')
        run('git pull')
        run('./manage.py collectstatic --noinput')
        run('uwsgi --reload {path}'.format(path=pid_file_path))
        run('service nginx restart')
