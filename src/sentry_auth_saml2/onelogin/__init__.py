from __future__ import absolute_import

from sentry.auth import register

from .provider import OneLoginSAML2Provider

register('onelogin', OneLoginSAML2Provider)
