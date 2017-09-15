#!/usr/bin/env python
"""
sentry-auth-saml2
=================
"""
from setuptools import setup, find_packages


install_requires = [
    'python3-saml>=1.2.3'
]

tests_require = [
    'flake8>=2.0,<2.1',
]

setup(
    name='sentry-auth-saml2',
    version='0.1.0.dev',
    author='Sentry',
    author_email='support@getsentry.com',
    url='https://www.getsentry.com',
    description='Generic SAML SSO provider for Sentry',
    long_description=__doc__,
    license='Apache 2.0',
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=['tests']),
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'tests': tests_require},
    include_package_data=True,
    entry_points={
        'sentry.apps': [
            'auth_saml2 = sentry_auth_saml2.generic',
            'auth_onelogin = sentry_auth_saml2.onelogin',
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
