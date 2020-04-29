"""
sentry_kavenegar.models
~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2016 by Matt Robenolt.
:license: BSD, see LICENSE for more details.
"""

import re
import phonenumbers

from django import forms
from django.utils.translation import ugettext_lazy as _

from kavenegar import *
from sentry import http
from sentry.plugins.bases.notify import NotificationPlugin

import sentry_kavenegar

DEFAULT_REGION = 'IR'
MAX_SMS_LENGTH = 160


def validate_phone(phone):
    try:
        p = phonenumbers.parse(phone, DEFAULT_REGION)
    except phonenumbers.NumberParseException:
        return False
    if not phonenumbers.is_possible_number(p):
        return False
    if not phonenumbers.is_valid_number(p):
        return False
    return True


def clean_phone(phone):
    # This could raise, but should have been checked with validate_phone first
    return phonenumbers.format_number(
        phonenumbers.parse(phone, DEFAULT_REGION),
        phonenumbers.PhoneNumberFormat.E164,
    )


def basic_auth(user, password):
    return 'Basic ' + (user + ':' + password).encode('base64').replace('\n', '')


def split_sms_to(data):
    return set(filter(bool, re.split(r'\s*,\s*|\s+', data)))


class KavenegarConfigurationForm(forms.Form):
    api_key = forms.CharField(label=_('API KEY'), required=True,
                              widget=forms.TextInput(attrs={'class': 'span6'}))
    sms_to = forms.CharField(label=_('SMS To #s'), required=True,
                             help_text=_('Recipient(s) phone numbers separated by commas or lines'),
                             widget=forms.Textarea(attrs={'placeholder': 'e.g. +98935XXXXXXX, 0912XXXXXXXX'}))

    def clean_sms_to(self):
        data = self.cleaned_data['sms_to']
        phones = split_sms_to(data)
        if len(phones) > 10:
            raise forms.ValidationError('Max of 10 phone numbers, {0} were given.'.format(len(phones)))
        for phone in phones:
            if not validate_phone(phone):
                raise forms.ValidationError('{0} is not a valid phone number.'.format(phone))
        return ','.join(sorted(map(clean_phone, phones)))

    def clean(self):
        # TODO: Ping Kavenegar and check credentials (?)
        return self.cleaned_data


class KavenegarPlugin(NotificationPlugin):
    author = 'Matt Robenolt'
    author_url = 'https://github.com/mattrobenolt'
    version = sentry_kavenegar.VERSION
    description = 'A plugin for Sentry which sends SMS notifications via Kavenegar'
    resource_links = (
        ('Documentation', 'https://github.com/amirasaran/sentry-kavenegar/blob/master/README.md'),
        ('Bug Tracker', 'https://github.com/amirasaran/sentry-kavenegar/issues'),
        ('Source', 'https://github.com/amirasaran/sentry-kavenegar'),
        ('Kavenegar', 'https://www.kavenegar.com/'),
    )

    slug = 'kavenegar'
    title = _('Kavenegar (SMS)')
    conf_title = title
    conf_key = 'kavenegar'
    project_conf_form = KavenegarConfigurationForm

    def is_configured(self, project, **kwargs):
        return all([self.get_option(o, project) for o in (
            'api_key', 'sms_to')])

    def get_send_to(self, *args, **kwargs):
        # This doesn't depend on email permission... stuff.
        return True

    def notify_users(self, group, event, **kwargs):
        project = group.project

        body = 'Sentry [{0}] {1}: {2}'.format(
            project.name.encode('utf-8'),
            event.get_level_display().upper().encode('utf-8'),
            event.error().encode('utf-8').splitlines()[0]
        )
        body = body[:MAX_SMS_LENGTH]

        api_key = self.get_option('api_key', project)

        sms_to = self.get_option('sms_to', project)
        if not sms_to:
            return
        sms_to = split_sms_to(sms_to)

        instance = KavenegarAPI(api_key)

        errors = []

        for phone in sms_to:
            if not phone:
                continue
            try:
                phone = clean_phone(phone)
                params = {
                    'receptor': phone,
                    'message': body
                }
                instance.sms_send(
                    params
                )
            except Exception as e:
                errors.append(e)

        if errors:
            if len(errors) == 1:
                raise errors[0]

            # TODO: multi-exception
            raise Exception(errors)
