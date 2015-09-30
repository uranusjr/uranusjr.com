#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import sqlite3
import sys


# Change dir to project root.
cur = os.path.abspath(os.path.dirname(__file__))
root = os.path.dirname(os.path.dirname(cur))
os.chdir(root)


def write_post(app, content, slug):
    if not isinstance(content, str):
        content = content.encode('utf-8')
    path = os.path.join(root, app, 'static', app, 'posts', slug) + '.md'
    with open(path, 'w') as f:
        f.write(content)


def main():
    app_name = sys.argv[1]
    model_name = sys.argv[2]
    table_name = (app_name + '_' + model_name).lower()
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('SELECT slug, content FROM {}'.format(table_name))
    row = c.fetchone()
    while row:
        slug, content = row
        write_post(app_name, content, slug)
        row = c.fetchone()


if __name__ == '__main__':
    main()
