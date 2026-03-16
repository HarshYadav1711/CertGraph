"""
Compatibility shim retained for tooling that might still import
``config.settings`` as a module.

The actual settings now live in ``config.settings.base`` and are exposed
via the ``config.settings`` package.
"""

from .settings.base import *  # noqa

