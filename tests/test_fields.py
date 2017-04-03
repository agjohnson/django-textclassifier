"""Test classifier fields"""

import json

import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase

from textclassifier.constants import SPAM, VALID
from textclassifier.models import TrainingData

from .models import Foobar


class TestFields(TestCase):

    def test_validator_no_data(self):
        m = Foobar.objects.create(foo='foo', bar='bar')
        try:
            m.clean_fields()
        except Exception:
            pytest.fail('Fields should have been clean')

    def test_validator_pass_empty_data(self):
        TrainingData.objects.create(
            app_label='tests',
            model='foobar',
            field_name='foo',
            data=None
        )
        m = Foobar.objects.create(foo='foo', bar='bar')
        try:
            m.clean_fields()
        except Exception:
            pytest.fail('Fields should have been clean')

    def test_validator_failure(self):
        TrainingData.objects.create(
            app_label='tests',
            model='foobar',
            field_name='foo',
            data=json.dumps([
                ('spam spam spam', SPAM),
                ('ham ham ham', VALID),
            ])
        )
        TrainingData.objects.create(
            app_label='tests',
            model='foobar',
            field_name='bar',
            data=json.dumps([
                ('foo foo foo', SPAM),
                ('bar bar bar', VALID),
            ])
        )
        m = Foobar.objects.create(
            foo='spam spam spam',
            bar='foo foo foo',
        )
        with self.assertRaises(ValidationError):
            m.clean_fields()
        m.foo = 'ham ham ham'
        with self.assertRaises(ValidationError):
            m.clean_fields()
        m.bar = 'bar bar bar'
        try:
            m.clean_fields()
        except Exception:
            pytest.fail('Fields should have been clean')
