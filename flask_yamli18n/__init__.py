#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''flask.ext.yamli18n
~~~~~~~~~~~~~~~~~~~~~

Use yaml files for i18n support in Flask framework.

:copyright: (c) 2012 by Lix Xu.
:license: BSD, see LICENSE for more details.

'''

import io
import os
import os.path
from collections import defaultdict
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from flask import session, request, Markup

__version__ = '0.1.5'


class YAMLI18N(object):
    def __init__(self, app=None, reload=None):
        '''reload controls whether reload the translations'''
        self.ymls = defaultdict(dict)
        self.ts = {}
        self.reload = reload
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        '''get the **locales** and **reload** setting:

            1. locales -> app.config['YAML_LOCALE_PATH']

            2. reload  -> app.config['YAML_RELOAD']
        '''
        locales_folder = app.config.get('YAML_LOCALE_PATH', 'locales')
        self.locales_path = os.path.join(app.root_path, locales_folder)
        if self.reload is None:
            self.reload = app.config.get('YAML_RELOAD', False)

        self.load_ymls()

    def load_ymls(self):
        '''load the translations to **self.ymls**'''
        if self.ymls and not self.reload:
            return

        for d in os.listdir(self.locales_path):
            if d.startswith('.'):
                continue

            d_path = os.path.join(self.locales_path, d)
            if os.path.isfile(d_path):
                continue

            for yml_file in os.listdir(d_path):
                if yml_file.endswith(('.yml', '.yaml')):
                    file_path = os.path.join(d_path, yml_file)
                    if self.reload:
                        mt = os.path.getmtime(file_path)
                        if self.ts.get(file_path) == mt:
                            continue

                    lang = os.path.splitext(yml_file)[0].lower()
                    with io.open(file_path, encoding='utf-8') as f:
                        self.ymls[d][lang] = load(f, Loader=Loader)

                    if self.reload:
                        self.ts[file_path] = mt

    def t(self, text, lang=None, failback='en', **kwargs):
        '''**text** follows the formats:

            1. name = default -> lang -> name

            2. .name = blueprint -> lang -> name

            3. ..name = blueprint -> lang -> endpoint -> name

            4. users.name = users_blueprint -> lang -> name

            5. users.edit.login = users_blueprint -> lang -> edit -> name

            in users/en.yml:

            .. sourcecode:: yaml

                .edit:
                    name: Hello, there

            **lang**
                You can specify  for direct translating

            **failback**
                if not translation files found for **lang**,
                use **failback** (default is `en`) instead

            **kwargs**
                used to provide additional params after translation

                e.g. the translation string is:

                .. sourcecode:: yaml

                    hello_world: {user}, Hello world

                then you can do this in your template:

                .. sourcecode:: html+jinja

                    {{ 'hello_world'|t(user='Lix') }}

                you will get:

                .. sourcecode:: html

                    Lix, Hello world
        '''

        self.load_ymls()
        if lang is None:
            lang = session.get('lang', 'en')

        if not text:
            return Markup(text)

        # is format 1
        if '.' not in text or (text[-1] == '.' and text.count('.') == 1):
            if lang not in self.ymls['default']:
                lang = failback

            if lang not in self.ymls['default']:
                return Markup(text)

            msg = self.ymls['default'][lang].get(text, text)
            return Markup(msg.format(**kwargs) if kwargs else msg)

        endpoint = None
        if text.startswith('..'):  # is format 3
            blueprint = request.blueprint
            endpoint = '.{0}'.format(request.endpoint.split('.')[-1])
            s = text[2:]
        elif text.startswith('.'):  # is format 2
            blueprint = request.blueprint
            s = text[1:]
        elif text.count('.') == 1:  # is format 4
            blueprint, s = text.split('.')
        else:  # is format 5
            blueprint, endpoint, s = text.split('.', 2)
            endpoint = '.' + endpoint

        if blueprint not in self.ymls:
            return Markup(text.format(**kwargs) if kwargs else text)

        bp = self.ymls[blueprint]
        if lang not in bp:
            lang = failback

        if lang not in bp:
            return Markup(text)

        yml = bp[lang]
        if endpoint in yml:
            msg = yml[endpoint].get(s, text)
            return Markup(msg.format(**kwargs) if kwargs else msg)

        if kwargs:
            return Markup(yml.get(s, text).format(**kwargs))

        return Markup(yml.get(s, text))
