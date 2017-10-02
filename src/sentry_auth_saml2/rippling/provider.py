from __future__ import absolute_import, print_function

from django import forms

from sentry.auth.providers.saml2 import SAML2Provider, Attributes
from sentry_auth_saml2.views import make_simple_setup
from sentry_auth_saml2.forms import URLMetadataForm


# Rippling specifically calls their Metadata URL a 'Issuer URL'
class RipplingURLMetadataForm(URLMetadataForm):
    metadata_url = forms.URLField(label='Issuer URL')


SelectIdP = make_simple_setup(
    RipplingURLMetadataForm,
    'sentry_auth_rippling/select-idp.html',
)


class RipplingSAML2Provider(SAML2Provider):
    name = 'Rippling'

    def get_saml_setup_pipeline(self):
        return [SelectIdP()]

    def attribute_mapping(self):
        return {
            Attributes.IDENTIFIER: 'TODO',
            Attributes.USER_EMAIL: 'TODO',
            Attributes.FIRST_NAME: 'TODO',
            Attributes.LAST_NAME: 'TODO',
        }
