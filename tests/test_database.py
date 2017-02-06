"""Test database classifier"""

import json

from django.core.exceptions import ValidationError
from django.test import TestCase

from textclassifier.classifier import DatabaseStorage
from textclassifier.validators import ClassifierValidator
from textclassifier.models import TrainingData

from .models import Foobar


class TestDatabaseClassifier(TestCase):

    def test_validator_pass_no_data(self):
        Foobar.objects.create(foo='foo', bar='bar')
        validate = ClassifierValidator(storage=DatabaseStorage('tests.foobar.foo'))
        self.assertTrue(validate('this is totally legit'))

    def test_validator_pass_empty_data(self):
        TrainingData.objects.create(
            field='tests.foobar.foo',
            data=None
        )
        Foobar.objects.create(foo='foo', bar='bar')
        validate = ClassifierValidator(storage=DatabaseStorage('tests.foobar.foo'))
        self.assertTrue(validate('this is totally legit'))

    def test_validator_failure(self):
        TrainingData.objects.create(
            field='tests.foobar.foo',
            data=json.dumps([('spam spam spam', 'spam'),
                             ('this is not spam', 'valid')])
        )
        validate = ClassifierValidator(storage=DatabaseStorage('tests.foobar.foo'))
        Foobar.objects.create(foo='spam spammy spam', bar='bar')
        with self.assertRaises(ValidationError):
            validate('spam spammy spam')
        self.assertTrue(validate('this is also not spam'))
