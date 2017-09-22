from __future__ import absolute_import, print_function

from django.core.urlresolvers import reverse

from sentry.auth.view import AuthView, ConfigureView
from sentry.auth.providers.saml2 import SAML2Provider
from sentry.utils.http import absolute_uri

from sentry_auth_saml2.forms import (
    SAMLForm,
    URLMetadataForm,
    XMLMetadataForm,
    process_metadata,
)


class SelectIdP(AuthView):
    def handle(self, request, helper):
        op = 'url'

        forms = {
            'url': URLMetadataForm(),
            'xml': XMLMetadataForm(),
            'idp': SAMLForm(),
        }

        if 'action_save' in request.POST:
            op = request.POST['action_save']
            form_cls = forms[op].__class__
            forms[op] = process_metadata(form_cls, request, helper)

        # process_metadata will return None when the action was successful and
        # data was bound to the helper.
        if not forms[op]:
            return helper.next_step()

        return self.respond('sentry_auth_saml2/select-idp.html', {
            'op': op,
            'forms': forms,
        })


class GenericSAML2ConfigureView(ConfigureView):
    def dispatch(self, request, organization, auth_provider):
        sp_metadata_url = absolute_uri(reverse('sentry-auth-organization-saml-metadata', args=[organization.slug]))
        data = auth_provider.config['idp']
        if request.POST:
            data = request.POST
            form = SAMLForm(data)
            if form.is_valid():
                idp_data = SAML2Provider.extract_idp_data_from_form(form)
                auth_provider.config['idp'] = idp_data
                auth_provider.save()
        else:
            form = SAMLForm(data)

        return self.render('sentry_auth_saml2/configure.html', {
            'sp_metadata_url': sp_metadata_url,
            'form': form
        })
