#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.utils.six.moves import html_parser, urllib
from django.utils.six.moves.urllib.error import URLError


class ForcedEnd(Exception):
    def __init__(self, og_image='', message=''):
        super(ForcedEnd, self).__init__(message)
        self.og_image = og_image


class OpenGraphImageParser(html_parser.HTMLParser):
    def parse_from_url(self, url):
        try:
            response = urllib.request.urlopen(url)
        except URLError:
            raise
        else:
            try:
                self.feed(response.read())
            except ForcedEnd as e:
                return e.og_image
        return ''

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'meta' and attrs.get('property') == 'og:image':
            try:
                og_image = attrs['content']
            except KeyError:    # Not a complete og:image tag; ignore.
                pass
            else:
                raise ForcedEnd(og_image)

    def handle_endtag(self, tag):
        if tag == 'head':   # Give up when we reached the end of head tags.
            raise ForcedEnd()
