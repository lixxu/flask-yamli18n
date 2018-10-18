"""
Flask-yamli18n
----------------

Use YAML files for i18n in Flask
It requires Python2.6+ as it uses string.format syntax.
Or you can modify it to python2.5 '%s' syntax.
"""
import os.path
from setuptools import setup

p = os.path.join(os.path.dirname(__file__), 'flask_yamli18n', '__init__.py')
with open(os.path.abspath(p)) as f:
    for line in f:
        if line.startswith('__version__ = '):
            version = line.split('=')[-1].strip().replace("'", '')
            break

setup(
    name='flask-yamli18n',
    version=version,
    url='https://github.com/lixxu/flask-yamli18n',
    license='BSD',
    author='Lix Xu',
    author_email='xuzenglin@gmail.com',
    description='Use yaml files as translation files in flask',
    long_description=__doc__,
    packages=['flask_yamli18n'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'PyYAML'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
