"""Test classifier fields"""

import json

from django.core.exceptions import ValidationError
from django.test import TestCase

from textclassifier.models import TrainingData

from .models import Foobar


class TestFields(TestCase):

    def test_validator_no_data(self):
        m = Foobar.objects.create(foo='foo', bar='bar')
        try:
            m.clean_fields()
        except Exception:
            self.fail()

    def test_validator_pass_empty_data(self):
        TrainingData.objects.create(
            field='tests.foobar.foo',
            data=None
        )
        m = Foobar.objects.create(foo='foo', bar='bar')
        try:
            m.clean_fields()
        except Exception:
            self.fail()

    def test_validator_failure(self):
        TrainingData.objects.create(
            field='tests.foobar.foo',
            data=json.dumps([('spam spam spam', 'spam'),
                             ('this is not spam', 'valid')])
        )
        TrainingData.objects.create(
            field='tests.foobar.bar',
            data=json.dumps([('scam scam scam', 'spam'),
                             ('this is not scam', 'valid')])
        )
        m = Foobar.objects.create(foo='spam spammy spam',
                                  bar='scam scammy scam')
        with self.assertRaises(ValidationError):
            m.clean_fields()
        m.foo = 'this is totally legit'
        with self.assertRaises(ValidationError):
            m.clean_fields()
        m.bar = 'this is totally legit'
        try:
            m.clean_fields()
        except Exception:
            self.fail()
