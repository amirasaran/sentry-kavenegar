"""
sentry_kavenegar
~~~~~~~~~~~~~

:copyright: (c) 2012 by Amir Asaran.
:license: BSD, see LICENSE for more details.
"""

try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('sentry-kavenegar').version
except Exception as e:
    VERSION = 'unknown'
