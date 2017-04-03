"""Test validators"""

import os
import sys
import json

from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings

from textclassifier.constants import SPAM, VALID
from textclassifier.models import TrainingData
from textclassifier.validators import TextClassificationValidator
from textclassifier.classifier import NaiveBayesClassifier


class TestValidators(TestCase):

    def setUp(self):
        self.data = [
            ('spam spam spam', SPAM),
            ('ham ham ham', VALID)
        ]
        self.training_data = TrainingData.objects.create(
            app_label='foo',
            model='bar',
            field_name='foobar',
            data=json.dumps(self.data)
        )

    def test_validator_pass(self):
        validate = TextClassificationValidator(
            app_label='foo',
            model='bar',
            field_name='foobar'
        )
        self.assertTrue(validate('ham ham ham'))

    def test_validator_invalid(self):
        validate = TextClassificationValidator(
            app_label='foo',
            model='bar',
            field_name='foobar'
        )
        with self.assertRaises(ValidationError):
            validate('spam spam spam')

    def test_validator_invalid_different_exception(self):
        validate = TextClassificationValidator(
            app_label='foo',
            model='bar',
            field_name='foobar',
            raises=ValueError
        )
        with self.assertRaises(ValueError):
            validate('spam spam spam')

    def test_invalid_json_throws_value_error(self):
        TrainingData.objects.create(
            app_label='foo',
            model='bar',
            field_name='invalid',
            data='null',
        )
        validate = TextClassificationValidator(
            app_label='foo',
            model='bar',
            field_name='invalid'
        )
        self.assertTrue(validate('spam spam spam'))

    def test_empty_json(self):
        TrainingData.objects.create(
            app_label='foo',
            model='bar',
            field_name='empty',
            data=None,
        )
        validate = TextClassificationValidator(
            app_label='foo',
            model='bar',
            field_name='empty'
        )
        self.assertTrue(validate('spam spam spam'))
