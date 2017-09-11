from __future__ import absolute_import, print_function

from django import forms
from onelogin.saml2.idp_metadata_parser import OneLogin_Saml2_IdPMetadataParser

from sentry.auth.view import AuthView, ConfigureView
from sentry.auth.providers.saml2 import SAML2Provider


class GenericSAML2ConfigureView(ConfigureView):
    def dispatch(self, request, organization, auth_provider):
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
            'form': form
        })


class SAMLForm(forms.Form):
    idp_entityid = forms.CharField(label='IdP Entity ID')
    idp_sso_url = forms.URLField(label='IdP Single Sign On URL')
    idp_slo_url = forms.URLField(label='IdP Single Log Out URL', required=False)
    idp_x509cert = forms.CharField(label='IdP x509 public certificate', widget=forms.Textarea)


class SelectIdPForm(SAMLForm):
    provider = forms.CharField(widget=forms.HiddenInput, initial='saml2', required=False)


class SelectIdP(AuthView):
    def handle(self, request, helper):
        error_url = error_xml = False
        url = xml = ''
        op = 'url'

        if 'action_save' in request.POST:
            op = 'idp'
            form = SelectIdPForm(request.POST)
            if form.is_valid():
                idp_data = SAML2Provider.extract_idp_data_from_form(form)

                helper.bind_state('idp', idp_data)
                helper.bind_state('contact', request.user.email)
                return helper.next_step()
        else:
            form = SelectIdPForm()
            if 'action_get_metadata' in request.POST or 'action_parse_metadata' in request.POST:
                if 'action_get_metadata' in request.POST:
                    op = 'url'
                    url = request.POST['idp_metadata_url']
                    error_url = True
                    if url:
                        try:
                            data = OneLogin_Saml2_IdPMetadataParser.parse_remote(url)
                        except:
                            data = None
                else:
                    op = 'xml'
                    xml = request.POST['idp_metadata_xml']
                    error_xml = True
                    if xml:
                        try:
                            data = OneLogin_Saml2_IdPMetadataParser.parse(xml)
                        except:
                            data = None
                if data and 'idp' in data:
                    idp_data = SAML2Provider.extract_idp_data_from_parsed_data(data)
                    form2 = SAMLForm(idp_data)
                    if form2.is_valid():
                        helper.bind_state('idp', idp_data)
                        helper.bind_state('contact', request.user.email)
                        return helper.next_step()

        return self.respond('sentry_auth_saml2/select-idp.html', {
            'op': op,
            'form': form,
            'error_url': error_url,
            'url': url,
            'error_xml': error_xml,
            'xml': xml
        })
