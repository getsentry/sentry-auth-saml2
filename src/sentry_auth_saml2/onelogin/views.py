from __future__ import absolute_import, print_function

from django import forms
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from sentry.auth.view import AuthView
from sentry.auth.providers.saml2 import (
    SAML2ConfigureView as BaseSAML2ConfigureView,
    NAMEID_FORMAT_CHOICES,
    AUTHNCONTEXT_CHOICES
)
from sentry.utils.http import absolute_uri
from sentry_auth_saml2.generic.views import SAMLForm, URLMetadataForm, process_metadata


class AdvancedForm(forms.Form):
    advanced_spentityid = forms.CharField(
        label='SP EntityID',
        required=False,
        help_text=_('Service Provider EntityID, if not provided, the URL where '
                    'Sentry publish the SP metadata will be used as its value')
    )
    advanced_nameidformat = forms.ChoiceField(
        label='NameID Format',
        required=False,
        choices=NAMEID_FORMAT_CHOICES,
        help_text=_('Specifies constraints on the name identifier to be used to '
                    'represent the requested subject. Review OneLogin metadata '
                    'to see the supported NameID formats')
    )
    advanced_requestedauthncontext = forms.MultipleChoiceField(
        label='Requested Authn Context',
        required=False,
        choices=AUTHNCONTEXT_CHOICES,
        help_text=_('AuthContext sent in the AuthNRequest. You can select none '
                    '(any authn source will be accepted), one or multiple '
                    'values')
    )
    advanced_sp_x509cert = forms.CharField(
        label='SP X.509 Certificate',
        widget=forms.Textarea,
        required=False,
        help_text=_('Public x509 certificate of the Service Provider')
    )
    advanced_sp_privatekey = forms.CharField(
        label='SP Private Key',
        widget=forms.Textarea,
        required=False,
        help_text=_('Private Key of the Service Provider')
    )

    def clean(self):
        super(AdvancedForm, self).clean()

        requires_sp_cert_data_due_enc = self.data.get('advanced_want_assertion_encrypted', False)
        has_sp_cert_data = self.data.get('advanced_sp_x509cert', None) and self.data.get('advanced_sp_privatekey', None)

        if requires_sp_cert_data_due_enc and not has_sp_cert_data:
            self._errors["advanced_sp_x509cert"] = [_("Required in order to be provided to OneLogin to let it encrypt")]
            self._errors["advanced_sp_privatekey"] = [_("Required in order to decrypt SAML data from OneLogin")]
            del self.cleaned_data["advanced_sp_x509cert"]
            del self.cleaned_data["advanced_sp_privatekey"]
        return self.cleaned_data


class OneLoginSAML2ConfigureView(BaseSAML2ConfigureView):
    saml_form_cls = SAMLForm
    advanced_form_cls = AdvancedForm

    def display_configure_view(self, organization, saml_form, options_form, attr_mapping_form, advanced_form):
        sp_metadata_url = absolute_uri(reverse('sentry-auth-organization-saml-metadata', args=[organization.slug]))

        return self.render('sentry_auth_onelogin/configure.html', {
            'sp_metadata_url': sp_metadata_url,
            'saml_form': saml_form,
            'options_form': options_form,
            'attr_mapping_form': attr_mapping_form,
            'advanced_form': advanced_form
        })


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
