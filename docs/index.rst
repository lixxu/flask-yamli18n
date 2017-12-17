.. Flask-YAMLI18N documentation master file, created by
   sphinx-quickstart on Tue Oct 16 16:15:46 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Flask-YAMLI18N |release| documentation
===========================================

.. module:: flask_yamli18n

Overview
---------
**Flask-YAMLI18N** is an i18n translation support for
`Flask`_ which is based on `PyYAML`_.
But, why not use `gettext`_?
Because gettext may need to install additional software (on Windows) which
I don't like.

Flask-YAMLI18N is simple and only for translating text
(without timezone support).
PS, this is from my personal project, so you can choose to use it or not.
You can try this great extension `Flask_Babel`_.

**Note**: Flask-YAMLI18N requires Python 2.6+ (uses **string.format** syntax).

.. todo:: more friendly document

.. highlight:: bash

Installation
------------------------

Install the extension with one of the following commands:::

  $ easy_install flask-yamli18n

or alternatively if you have pip installed::

  $ pip install flask-yamli18n

Configuration
-------------------------

+--------------------+------------------------------------------+
|**YAML_LOCALE_PATH**| Define the location folder for yml files.|
|                    | (default is **locales**)                 |
+--------------------+------------------------------------------+
|**YAML_RELOAD**     | If reload the translation when files     |
|                    | modified. (default is **False**)         |
+--------------------+------------------------------------------+

How to use
------------
In your Flask application file (e.g. hello.py)::

    from flask import Flask, session, request
    from flask_yamli18n import YAMLI18N

    app = Flask(__name__)
    y18n = YAMLI18N(app)
    # or later
    # y18n = YAMLI18N()
    # y18n.init_app(app)

    t = y18n.t  # for short

    # default translation files folder is 'locales'
    # app.config['YAML_LOCALE_PATH'] = 'locales'

    app.jinja_env.filters['t'] = t
    # or if you want use it as function
    # app.jinja_env.globals['_'] = t

    # put lang to your session
    @app.before_request
    def load_lang():
        if 'lang' not in session:
            session['lang'] = request.accept_languages.best

**Example folder structure**::

    /hello.py
    /locales
        /default
            /en.yml
            /zh.yml
        /blueprint_a
            /en.yml
            /zh.yml

the **blueprint_a** is get from::

    mod = Blueprint('blueprint_a', __name__)

    @mod.route('/')
    def index():
        return render_template('hello.html')

suppose you have a **users** blueprint, then the structure is::

    /default
        /en.yml
        /zh.yml
    /users
        /en.yml
        /zh.yml

**locales/default/en.yml** example:

.. sourcecode:: yaml

    hello: Hello  # or 'Hello' or "Hello"
    hello_world: "Hello, World!"

In your template file (e.g. **hello.html**):

.. sourcecode:: html+jinja

    <!doctype html>
    <title>{{ 'hello'|t }}</title>
    {{ 'hello_world'|t }}

The output is:

.. sourcecode:: html

    <!doctype html>
    <title>Hello</title>
    Hello, World!

API
------------------

.. autoclass:: YAMLI18N
   :members:

.. toctree::
   :maxdepth: 2

.. _Flask: http://flask.pocoo.org/
.. _babel: http://babel.edgewall.org/
.. _pytz: http://pytz.sourceforge.net/
.. _speaklater: http://pypi.python.org/pypi/speaklater
.. _PyYAML: http://pyyaml.org/
.. _gettext: http://www.gnu.org/software/gettext/
.. _Flask_Babel: http://packages.python.org/Flask-Babel/

Changelog
---------

Version 0.1.8
-------------

(bug fixed, released on 2017-Dec-17)

- KeyError for `kwargs`


Version 0.1.7
-------------

(tiny improvement, released on 2017-Oct-27)

- moved `lang` and `failback` to `kwargs`, and added `args` for `t` method.


Version 0.1.5
-------------

(tiny improvement, released on 2017-Oct-26)

- Use `io` module to open the yaml files with encoding `utf-8` to work in python3.


Version 0.1.4
-------------

(tiny improvement, released on 2015-Jan-23)

- Use `<http://flask.pocoo.org/docs/0.10/api/#flask.Markup>`_ for returned translation text
  so that template no need to use `safe` filter any more.
