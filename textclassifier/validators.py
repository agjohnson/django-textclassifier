"""Text classification validator"""

import logging

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _

from .constants import VALID, SPAM
from .classifier import DefaultClassifier

log = logging.getLogger(__name__)


@deconstructible
class ClassifierValidator(object):
    """Text classifier validator

    Validator that uses classifier to for validation. By default, this uses a
    naive bayesian classification and looks for the file configured with the
    setting :py:data:`TEXTCLASSIFIER_DATA_FILE`. If there is a problem with this
    file, a warning is throw and validation will succeed.

    To avoid raising a validation error to users, you can specify a different
    exception with ``raises``. Form validation or saving can then be wrapped to
    catch this new exception and mimic form processing/instance saving, useful
    for shadowbanning users.

    :param raises: Exception class to raise on invalid data
    :param type: class
    :param message: Message to raise on exception
    :param code: Validation error code to raise with :py:cls:`ValidationError`
    """

    exception_class = ValidationError
    message = _('Invalid content')
    code = 'invalid'

    def __init__(self, raises=None, message=None, code=None):
        if raises is not None:
            self.exception_class = raises
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        self.classifier = self.get_classifier()
        if self.classifier is None:
            return
        pdist = self.classifier.prob_classify(value)
        if pdist.prob(SPAM) > 0.90:
            log.debug('Classification failed (valid=%.2f spam=%.2f)',
                      pdist.prob(VALID), pdist.prob(SPAM))
            if issubclass(self.exception_class, ValidationError):
                raise self.exception_class(self.message, self.code)
            else:
                raise self.exception_class(self.message)

    def __eq__(self, other):
        """Compare for serialization"""
        return (
            isinstance(other, ClassifierValidator) and
            other.classifier == self.classifier and
            other.raises == self.raises
        )

    def __ne__(self, other):
        """Inverse compare for serialization"""
        return not (self == other)

    def get_classifier(self):
        try:
            return DefaultClassifier()
        except (IOError, OSError, ValueError):
            log.warn('Error initializing classifier data, check data file',
                     exc_info=True)


validate_classification = ClassifierValidator()
