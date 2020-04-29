#!/usr/bin/env python
"""
sentry-kavenegar
=============

A plugin for Sentry which sends SMS notifications via Kavenegar.

:copyright: (c) 2012 by Matt Robenolt
:license: BSD, see LICENSE for more details.
"""
from setuptools import setup, find_packages


install_requires = [
    'sentry>=7.0.0',

    # We don't need full `phonenumbers` library
    'phonenumberslite<8.0',
    'kavenegar>=1.1.2',
]

setup(
    name='sentry-kavenegar',
    version='0.1.0',
    author='Amir Asaran',
    author_email='admin@mihanmail.com',
    url='https://github.com/amirasaran/sentry-kavenegar',
    description='A plugin for Sentry which sends SMS notifications via Kaveneger',
    long_description=__doc__,
    license='BSD',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        'sentry.apps': [
            'kavenegar = sentry_kavenegar',
        ],
        'sentry.plugins': [
            'kavenegar = sentry_kavehnegar.models:KavenegarPlugin',
        ]
    },
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
