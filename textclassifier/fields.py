"""Classifier TextField implementation"""

from django.db.models.fields import TextField

from .classifier import DatabaseStorage
from .validators import ClassifierValidator


class ClassifierTextField(TextField):
    """Implementation of TextField that uses classification for validation

    This is mostly a helper function that eliminates the need to specify the
    lookup query in the classification model
    """

    storage_class = DatabaseStorage

    def __init__(self, *args, **kwargs):
        storage_class = kwargs.pop('storage_class', None)
        if storage_class is not None:
            self.storage_class = storage_class
        super(ClassifierTextField, self).__init__(*args, **kwargs)

    @property
    def validators(self):
        # pylint: disable=protected-access, unnecessary-lambda
        validator_list = list(self._validators)
        field_name = '.'.join([self.model._meta.app_label,
                               self.model._meta.model_name,
                               self.name])
        validator_list.append(
            lambda value: ClassifierValidator(
                storage=self.storage_class(field_name),
            )(value)
        )
        return validator_list
