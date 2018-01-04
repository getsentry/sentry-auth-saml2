# SAML2 Auth for Sentry

*Note:* SAML2 Authenttication is still currently an experimental feature.

An SSO provider for Sentry which enables SAML SSO and SLO support, including
various identity provider support.

The following identity providers are supported

 * [OneLogin](https://www.onelogin.com/)
 * [Okta](https://www.okta.com/)
 * [Auth0](https://auth0.com/)
 * [Rippling](https://rippling.com/)

A generic SAML2 module is also provided, which may be configured with any
Identity Provider that conforms to the SAML2 specification.

## Install

```
$ pip install https://github.com/getsentry/sentry-auth-saml2/archive/master.zip
```

## Configuration

Refer to the Sentry [Single Sign-On
documentation](https://docs.sentry.io/learn/sso/) for individual SAML Identity
Provider configurations.

Refer to the [Enabling SSO
documentation](https://github.com/getsentry/sentry/blob/18a8600610866d22b71f420c52b04272581c7799/docs/sso.rst#enabling-sso)
for what feature flags to enable for this plugin.
