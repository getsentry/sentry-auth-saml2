from __future__ import absolute_import

from sentry.auth import register

from .provider import GenericSAML2Provider

register('saml2', GenericSAML2Provider)