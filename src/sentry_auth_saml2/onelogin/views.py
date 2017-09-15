from __future__ import absolute_import, print_function

from django import forms
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import URLValidator

from onelogin.saml2.idp_metadata_parser import OneLogin_Saml2_IdPMetadataParser

from sentry.auth.view import AuthView, ConfigureView
from sentry.auth.providers.saml2 import SAML2Provider
from sentry.utils.http import absolute_uri


class OneLoginSAML2ConfigureView(ConfigureView):
    def dispatch(self, request, organization, auth_provider):
        if request.POST:
            data = request.POST
            form = SAMLForm(data)
            form2 = AttributeMappingForm(data)
            if form.is_valid():
                idp_data = SAML2Provider.extract_idp_data_from_form(form)
                auth_provider.config['idp'] = idp_data
                auth_provider.save()
            if form2.is_valid():
                attribute_mapping_data = SAML2Provider.extract_attribute_mapping_from_form(form2)
                auth_provider.config['attribute_mapping'] = attribute_mapping_data
                auth_provider.save()
        else:
            data = auth_provider.config['idp']
            form = SAMLForm(data)

            data2 = None
            if 'attribute_mapping' in auth_provider.config:
                data2 = auth_provider.config['attribute_mapping']
            form2 = AttributeMappingForm(data2)

        sp_metadata_url = absolute_uri(reverse('sentry-auth-organization-saml-metadata', args=[organization.slug]))

        return self.render('sentry_auth_onelogin/configure.html', {
            'sp_metadata_url': sp_metadata_url,
            'form': form,
            'form2': form2,
        })


class SAMLForm(forms.Form):
    idp_entityid = forms.CharField(label='OneLogin Entity ID', help_text="Issuer URL")
    idp_sso_url = forms.URLField(label='OneLogin Single Sign On URL', help_text="SAML 2.0 Endpoint (HTTP)")
    idp_slo_url = forms.URLField(label='OneLogin Single Log Out URL', required=False, help_text="SLO Endpoint (HTTP)")
    idp_x509cert = forms.CharField(label='OneLogin x509 public certificate', widget=forms.Textarea, help_text="X.509 Certificate")


class AttributeMappingForm(forms.Form):
    attribute_mapping_email = forms.CharField(label='Email')
    attribute_mapping_firstname = forms.CharField(label='First Name', required=False)


class SelectIdP(AuthView):
    def handle(self, request, helper):
        error_value = error_url = False
        metadata_url = url = ''
        if 'action_save' in request.POST:
            metadata_url = request.POST['metadata_url']

            validate_url = URLValidator()
            try:
                validate_url(metadata_url)
                url = metadata_url
                try:
                    data = OneLogin_Saml2_IdPMetadataParser.parse_remote(url)

                    if data and 'idp' in data:
                        idp_data = SAML2Provider.extract_idp_data_from_parsed_data(data)
                        form2 = SAMLForm(idp_data)
                        if form2.is_valid():
                            helper.bind_state('idp', idp_data)
                            helper.bind_state('contact', request.user.email)
                            return helper.next_step()
                except Exception:
                    error_url = True
            except ValidationError:
                error_value = True

        return self.respond('sentry_auth_onelogin/select-idp.html', {
            'error_value': error_value,
            'error_url': error_url,
            'metadata_url': metadata_url
        })
