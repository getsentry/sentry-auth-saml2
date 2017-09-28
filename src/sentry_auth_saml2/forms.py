from __future__ import absolute_import

from django import forms
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _
from onelogin.saml2.idp_metadata_parser import OneLogin_Saml2_IdPMetadataParser


def extract_idp_data_from_parsed_data(data):
    """
    Transform data returned by the OneLogin_Saml2_IdPMetadataParser into the
    expected IdP dict shape.
    """
    idp = data.get('idp', {})

    return {
        'entity_id': idp.get('entityId'),
        'sso_url': idp.get('singleSignOnService', {}).get('url'),
        'slo_url': idp.get('singleLogoutService', {}).get('url'),
        'x509cert': idp.get('x509cert'),
    }


def process_url(form):
    url = form.cleaned_data['metadata_url']
    data = OneLogin_Saml2_IdPMetadataParser.parse_remote(url)
    return extract_idp_data_from_parsed_data(data)


def process_xml(form):
    xml = form.cleaned_data['metadata_xml']
    data = OneLogin_Saml2_IdPMetadataParser.parse(xml)
    return extract_idp_data_from_parsed_data(data)


class URLMetadataForm(forms.Form):
    metadata_url = forms.URLField(label='Metadata URL')
    processor = process_url


class XMLMetadataForm(forms.Form):
    metadata_xml = forms.CharField(label='Metadata XML', widget=forms.Textarea)
    processor = process_xml


class SAMLForm(forms.Form):
    entity_id = forms.CharField(label='Entity ID')
    sso_url = forms.URLField(label='Single Sign On URL')
    slo_url = forms.URLField(label='Single Log Out URL', required=False)
    x509cert = forms.CharField(label='x509 public certificate', widget=forms.Textarea)
    processor = lambda d: d


def process_metadata(form_cls, request, helper):
    form = form_cls()

    if 'action_save' not in request.POST:
        return form

    form = form_cls(request.POST)

    if not form.is_valid():
        return form

    try:
        data = form_cls.processor(form)
    except Exception:
        errors = form._errors.setdefault('__all__', ErrorList())
        errors.append('Failed to parse provided SAML2 metadata')
        return form

    saml_form = SAMLForm(data)
    if not saml_form.is_valid():
        return form

    helper.bind_state('idp', data)
    helper.bind_state('contact', request.user.email)

    # Data is bound, do not respond with a form to signal the nexts steps
    return None
