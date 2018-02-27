"""Text classification validator"""

import logging

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _

from .classifier import NaiveBayesClassifier

log = logging.getLogger(__name__)


@deconstructible
class TextClassificationValidator(object):
    """Text classifier validator

    Field validator that uses a text classifier for validation. Training data is
    stored in a database table on a per-field basis.

    To avoid raising a validation error to users, you can specify a different
    exception with ``raises``. Form validation or saving can then be wrapped to
    catch this new exception and mimic form processing/instance saving, useful
    for shadowbanning users.

    :param raises: Exception class to raise on invalid data
    :param message: Message to raise on exception
    :param code: Validation error code to raise with :py:cls:`ValidationError`
    :param field_name: Field name to use in database field lookup
    """

    exception_class = ValidationError
    message = _('Invalid content')
    code = 'invalid'

    def __init__(self, raises=None, message=None, code=None, app_label=None,
                 model=None, field_name=None):
        if raises is not None:
            self.exception_class = raises
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        self.classifier = NaiveBayesClassifier(
            app_label=app_label,
            model=model,
            field_name=field_name,
        )

    def __call__(self, value):
        self.classifier.load()
        result = self.classifier.classify(value)
        if result.is_spam():
            if issubclass(self.exception_class, ValidationError):
                raise self.exception_class(self.message, self.code)
            else:
                raise self.exception_class(self.message)
        return True

    def __eq__(self, other):
        """Compare for serialization"""
        return (
            isinstance(other, TextClassificationValidator) and
            other.classifier == self.classifier and
            other.exception_class == self.exception_class and
            other.code == self.code and
            other.message == self.message
        )

    def __ne__(self, other):
        """Inverse compare for serialization"""
        return not (self == other)
