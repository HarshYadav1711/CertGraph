"""
Settings package for the certgraph Django project.

The base settings live in ``base.py`` and are imported here so that
``DJANGO_SETTINGS_MODULE='config.settings'`` continues to work. Additional
environment-specific modules (for example ``dev.py`` or ``prod.py``) can be
added later without changing the entrypoint.
"""

from .base import *  # noqa

