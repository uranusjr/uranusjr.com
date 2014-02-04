#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
import os.path
from contextlib import wraps
from distutils.util import strtobool
from six.moves import configparser
from fabric.api import cd, run
from fabric.decorators import task
from fabric.operations import prompt


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
def deploy(extras='restart'):
    """General deploy task

    The extra argument goes like this:

        fab deploy:extras=migrate,restart

    Which will be roughly equivalent to

        deploy()
        migrate()
        restart()

    By default "restart" will be invoked. Passing an string overrides it.
    """
    # Parse extra tasks
    funcs = []
    failed_lookups = []
    for func_name in extras.split(' '):
        try:
            func = globals()[func_name]
        except KeyError:
            failed_lookups.append(func_name)
        else:
            funcs.append(func)
    if failed_lookups:
        msg_form = (
            'The following tasks does not seem to exist: {names}. Continue '
            'anyway? '
        )
        should_continue = prompt(
            msg_form.format(names=', '.join(failed_lookups)),
            default='n',
            validate=strtobool
        )
        if not bool(strtobool(should_continue)):
            print('Aborting.')
            return

    run('git reset HEAD --hard')
    run('git pull')
    run('./manage.py collectstatic --noinput')
    for func in funcs:
        func()


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
