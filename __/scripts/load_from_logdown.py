#!/usr/bin/env python
# -*- coding: utf-8

from __future__ import unicode_literals
import os
import contextlib
import datetime
import re
import tempfile
import zipfile
from django import forms
from django.utils.html import strip_tags
from django.utils.text import slugify
from django.utils.timezone import utc
from blog.models import Post, Tag


@contextlib.contextmanager
def chdir(dirname):
    """Context manager for changing the current working directory temporarily
    """
    cwd = os.getcwd()
    try:
        os.chdir(dirname)
        yield
    except:
        os.chdir(cwd)
        raise
    else:
        os.chdir(cwd)


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Post


class BlogTagForm(forms.ModelForm):
    class Meta:
        model = Tag


class Converter(object):

    def process(self, zip_path):
        with chdir(self.unzip(zip_path)):
            self.full_convert()

    def unzip(self, zip_path):
        zip_path = os.path.abspath(zip_path)
        try:
            assert zipfile.is_zipfile(zip_path)
        except AssertionError:
            raise RuntimeError(
                '{fn} is not a ZIP file.'.format(fn=zip_path)
            )

        target_name = os.path.splittext(os.path.basename(zip_path))
        temp_dir_path = os.path.join(tempfile.gettempdir(), target_name)
        os.makedirs(temp_dir_path)
        with zipfile.ZipFile(zip_path) as zip_file:
            zip_file.extractall(temp_dir_path)
        return temp_dir_path

    def full_convert(self, basedir='.'):
        md_files = sorted([
            fn for fn in os.listdir(basedir)
            if fn.endswith('.md')
        ])
        for md in md_files:
            with open(md) as f:
                # Start of header
                line = f.readline().strip()
                if line != '---':
                    raise RuntimeError(
                        'Malformed file {fn}. Expecting "---" (first line), '
                        'but got {line}'.format(fn=md, line=line)
                    )

                form_data = {}

                # Read the header
                line = f.readline().strip()
                while line != '---':
                    key, value = [c.strip() for c in line.split(':')]

                    # Each header field should implement a method of its
                    # name prefixed with "convert_". Each of these methods
                    # should take the value as the argument, and returns
                    # a tuple (form_field_name, value_to_use).
                    try:
                        method = getattr(self, 'convert_' + key)
                    except AttributeError:
                        continue
                    field_name, field_value = method(value)
                    if field_name:
                        form_data[field_name] = field_value

                # Read the content (i.e. rest of the file)
                content = f.read()
                form_data['content'] = content

                # Other needed things
                # TODO: Need unicode_slugify
                form_data['slug'] = slugify(form_data['title'])
                # TODO: WE NEED A CATEGORY

                # Save the object now to make Markdown render to HTML
                post = BlogPostForm(initial=form_data).save()

                # If there is a <!--more--> tag, use the content before it as
                # the short_description value
                # TODO: Should use a real HTML-parser
                match = re.search(r'<!--\s*more\s*-->')
                if match:
                    short_description = strip_tags(content[:match.start()])
                    post.short_description = short_description
                    post.save(update_fields=('short_description'),)

    def convert_layout(self, value):
        return (None, None)

    def convert_title(self, value):
        return ('title', value.strip("'"))

    def convert_date(self, value):
        dt = datetime.strptime(value, '%Y-%M-%d %H:%M').replace(tzinfo=utc)
        return ('published_at', dt)

    def convert_comments(self, value):
        return (None, None)

    def convert_categories(self, value):
        tags = []
        for tag_name in value.lstrip('[').rstrip(']').split(','):
            tag_name = tag_name.strip()
            try:
                tag = Tag.objects.get(name__iexact=tag_name)
            except Tag.DoesNotExist:
                tag = BlogTagForm(initial={
                    'name': tag_name, 'slug': slugify(tag_name)
                }).save()
            tags.append(tag)
        return ('tags', tags)
