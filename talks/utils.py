#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.utils.six.moves import html_parser, urllib


class ForcedEnd(Exception):
    pass


class OpenGraphImageParser(html_parser.HTMLParser):
    def parse_from_url(self, url):
        self.og_image = None
        try:
            response = urllib.request.urlopen(url)
        except urllib.error.URLError:
            return
        else:
            try:
                self.feed(response.read())
            except ForcedEnd:
                pass

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'meta' and attrs.get('property') == 'og:image':
            try:
                self.og_image = attrs['content']
            except KeyError:    # Not a complete og:image tag; ignore.
                pass
            else:
                raise ForcedEnd

    def handle_endtag(self, tag):
        if tag == 'head':   # Give up when we reached the end of head tags.
            raise ForcedEnd
