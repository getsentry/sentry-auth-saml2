from __future__ import absolute_import

from sentry.auth import register

from .provider import OktaSAML2Provider

register('okta', OktaSAML2Provider)
