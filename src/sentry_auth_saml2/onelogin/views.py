from __future__ import absolute_import, print_function

from django import forms

from sentry.auth.view import AuthView
from sentry_auth_saml2.forms import URLMetadataForm, process_metadata


# Onelogin specifically calls their Metadata URL a 'Issuer URL'
class OneLoginURLMetadataForm(URLMetadataForm):
    metadata_url = forms.URLField(label='Issuer URL')


class SelectIdP(AuthView):
    def handle(self, request, helper):
        form = process_metadata(OneLoginURLMetadataForm, request, helper)

        if form:
            return self.respond('sentry_auth_onelogin/select-idp.html', {'form': form})
        else:
            return helper.next_step()
