#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os.path
from contextlib import wraps
from six.moves import configparser
from fabric.api import cd, run
from fabric.decorators import task


try:
    ConfigParser = configparser.SafeConfigParser
except AttributeError:  # Python 3 renames SafeConfigParser to ConfigParser
    ConfigParser = configparser.ConfigParser


def get_uwsgi_config(key):
    if not hasattr(get_uwsgi_config, '_config'):
        ini_path = os.path.join(os.path.dirname(__file__), 'uwsgi.ini')
        get_uwsgi_config._config = ConfigParser()
        get_uwsgi_config._config.read(ini_path)
    return get_uwsgi_config._config.get('uwsgi', key)


def project(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        with cd(get_uwsgi_config('chdir')):
            func(*args, **kwargs)

    return wrapper


@task
@project
def deploy(with_restart=True):
    run('git reset HEAD --hard')
    run('git pull')
    run('./manage.py collectstatic --noinput')
    if with_restart:
        restart()


@task
@project
def migrate():
    run('./manage.py syncdb')
    run('./manage.py migrate')


@task
def restart():
    pid_file_path = get_uwsgi_config('pidfile')
    run('uwsgi --reload {path}'.format(path=pid_file_path))
    run('service nginx restart')
