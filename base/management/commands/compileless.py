#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.management.utils import find_command, popen_wrapper


class Command(BaseCommand):
    def handle(self, *args, **options):
        BASE_STATIC = os.path.join(
            settings.BASE_DIR, 'base', 'static', 'base'
        )
        program = 'lessc'
        if find_command(program) is None:
            raise CommandError(
                'You need to install the LESS compiler (lessc) to use this '
                'command.'
            )
        args = [
            program,
            os.path.join(BASE_STATIC, 'less', 'import.less'),
            os.path.join(BASE_STATIC, 'css', 'style.css'),
        ]
        output, errors, status = popen_wrapper(args)
        if status:
            if errors:
                msg = '{program} execution failed: {errors}'
            else:
                msg = '{program} execution failed without error output.'
            msg = msg.format(program=program, errors=errors)
            raise CommandError(msg)
