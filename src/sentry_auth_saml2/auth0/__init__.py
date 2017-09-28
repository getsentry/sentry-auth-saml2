from __future__ import absolute_import

from sentry.auth import register

from .provider import Auth0SAML2Provider

register('auth0', Auth0SAML2Provider)
