from __future__ import absolute_import, print_function

from sentry.auth.providers.saml2 import SAML2Provider

from .views import (
    OneLoginSAML2ConfigureView, SelectIdP
)

from .constants import ONELOGIN_EMAIL, ONELOGIN_DISPLAYNAME


class OneLoginSAML2Provider(SAML2Provider):
    name = 'OneLogin'

    def get_configure_view(self):
        return OneLoginSAML2ConfigureView.as_view()

    def get_setup_pipeline(self):
        return [
            SelectIdP()
        ]

    def build_config(self, state):
        data = super(OneLoginSAML2Provider, self).build_config(state)

        if data:
            data['attribute_mapping'] = {
                'attribute_mapping_email': ONELOGIN_EMAIL,
                'attribute_mapping_displayname': ONELOGIN_DISPLAYNAME,
            }
        return data
