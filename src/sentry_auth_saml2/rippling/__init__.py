from __future__ import absolute_import

from sentry.auth import register

from .provider import RipplingSAML2Provider

register('rippling', RipplingSAML2Provider)
