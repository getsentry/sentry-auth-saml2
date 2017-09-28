from __future__ import absolute_import, print_function

from sentry.auth.providers.saml2 import SAML2Provider, Attributes

from .views import SelectIdP


class OneLoginSAML2Provider(SAML2Provider):
    name = 'OneLogin'

    def get_saml_setup_pipeline(self):
        return [SelectIdP()]

    def attribute_mapping(self):
        return {
            Attributes.IDENTIFIER: 'PersonImmutableID',
            Attributes.USER_EMAIL: 'User.email',
            Attributes.FIRST_NAME: 'User.FirstName',
            Attributes.LAST_NAME: 'User.LastName',
        }
