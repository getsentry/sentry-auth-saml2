from __future__ import absolute_import

import django

if django.VERSION[:2] >= (1, 8):
    # Django 1.9 specifically requires that models not be imported before setup,
    # which sentry.auth does, so we need to use AppConfig here.
    # Also works on 1.8.
    default_app_config = "sentry_auth_saml2.generic.apps.Config"
else:
    # Provide backwards compatibility.
    from sentry.auth import register

    from .provider import GenericSAML2Provider

    register('saml2', GenericSAML2Provider)
