"""Test validators"""

import os
import sys
import json

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

# First load settings
import mock
from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from textblob.classifiers import NaiveBayesClassifier

from textclassifier.validators import ClassifierValidator
from textclassifier.classifier import FileStorage


class TestValidators(TestCase):

    def setUp(self):
        self.data = json.dumps([
            ('spam spam spam', 'spam'),
            ('this is not spam', 'valid')
        ])
        self.mocks = {
            'open': mock.patch(
                'textclassifier.classifier.open',
                mock.mock_open(read_data=self.data),
                create=True,
            ),
        }
        self.patches = dict((k, m.start()) for (k, m) in self.mocks.items())

    def test_validator_pass(self):
        validate = ClassifierValidator(storage=FileStorage('/dev/null'))
        self.assertTrue(validate('this is totally legit'))

    def test_validator_invalid(self):
        validate = ClassifierValidator(storage=FileStorage('/dev/null'))
        with self.assertRaises(ValidationError):
            validate('spam spammy spam')

    def test_validator_invalid_different_exception(self):
        validate = ClassifierValidator(storage=FileStorage('/dev/null'),
                                       raises=ValueError)
        with self.assertRaises(ValueError):
            validate('spam spammy spam')

    def test_invalid_json_throws_value_error(self):
        self.patches['open'].return_value.read.return_value = 'INVALID JSON'
        validate = ClassifierValidator(storage=FileStorage('/dev/null'))
        with self.assertRaises(ValueError):
            validate('spam spammy spam')

    def test_empty_json(self):
        self.patches['open'].return_value.read.return_value = '[]'
        validate = ClassifierValidator(storage=FileStorage('/dev/null'))
        self.assertTrue(validate('spam spammy spam'))

    def test_open_file_failure_reraises_exception(self):
        """Open file, but still validate after errors"""
        self.patches['open'].side_effect = IOError
        validate = ClassifierValidator(storage=FileStorage('/dev/null'))
        with self.assertRaises(IOError):
            validate('this is totally legit')
