"""Text classification validator"""

import logging

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _

from .constants import VALID, SPAM

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
    :param classifier_class: Classifier class
    """

    exception_class = ValidationError
    message = _('Invalid content')
    code = 'invalid'

    def __init__(self, raises=None, message=None, code=None,
                 storage=None):
        if raises is not None:
            self.exception_class = raises
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        self.storage = storage

    def __call__(self, value):
        classifier = self.storage.load()
        try:
            pdist = classifier.prob_classify(value)
        except ValueError:
            # If the training data is incomplete, calls to prob_classify will
            # throw an exception on not having enough bins
            return True
        if pdist.prob(SPAM) > 0.90:
            log.debug('Classification failed (valid=%.2f spam=%.2f)',
                      pdist.prob(VALID), pdist.prob(SPAM))
            if issubclass(self.exception_class, ValidationError):
                raise self.exception_class(self.message, self.code)
            else:
                raise self.exception_class(self.message)
        return True

    def __eq__(self, other):
        """Compare for serialization"""
        return (
            isinstance(other, ClassifierValidator) and
            other.storage == self.storage and
            other.raises == self.raises
        )

    def __ne__(self, other):
        """Inverse compare for serialization"""
        return not (self == other)


validate_classification = ClassifierValidator()
