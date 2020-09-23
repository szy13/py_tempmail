from setuptools import setup, find_packages
from os.path import join, dirname

import tempmail

attrs = {
    'name': tempmail.__name__,
    'version': tempmail.__version__,
    'author': tempmail.__author__,
    'author_email': tempmail.__email__,
    'url': tempmail.__url__,
    'long_description': open(join(dirname(__file__), 'README.md')).read(),
    'packages': find_packages(),
    'install_requires': [
        'requests',
        'bs4'
    ]
}

setup(**attrs)
