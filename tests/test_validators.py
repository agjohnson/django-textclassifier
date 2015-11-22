"""Test validators"""

import sys

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
from textclassifier.classifier import DefaultClassifier


class TestValidators(TestCase):

    def setUp(self):
        self.data = StringIO('{}')
        self.classifier = NaiveBayesClassifier(self.data, format='json')
        self.classifier.update([
            ('spam spam spam', 'spam'),
            ('this is not spam', 'valid'),
        ])

        self.mock_classifier_get = mock.patch.object(
            ClassifierValidator,
            'get_classifier',
            mock.Mock(return_value=self.classifier)
        )
        self.patch_classifier_get = self.mock_classifier_get.start()

    def test_validator_pass(self):
        validate = ClassifierValidator()
        validate('this is totally legit')

    def test_validator_invalid(self):
        validate = ClassifierValidator()
        with self.assertRaises(ValidationError):
            validate('spam spammy spam')

    def test_validator_invalid_different_exception(self):
        validate = ClassifierValidator(raises=ValueError)
        with self.assertRaises(ValueError):
            validate('spam spammy spam')

    @mock.patch('textclassifier.classifier.TEXTCLASSIFIER_DATA_FILE', '')
    def test_open_file_failure(self):
        """Open file, but still validate after errors"""
        self.mock_classifier_get.stop()
        mod_name = ('builtins', '__builtin__')[(sys.version_info < (3,0))]
        with mock.patch('{0}.open'.format(mod_name)) as mocked_open:
            mocked_open.side_effect = IOError
            with self.assertRaises(IOError):
                DefaultClassifier()
            validate = ClassifierValidator()
            validate('spam spam spam')
