"""Classifier TextField implementation"""

from django.db.models.fields import TextField

from .validators import TextClassificationValidator


class TextClassificationField(TextField):
    """Implementation of TextField that uses classification for validation

    This is mostly a helper function that eliminates the need to specify the
    lookup query in the classification model
    """

    @property
    def validators(self):
        # pylint: disable=protected-access, unnecessary-lambda
        validator_list = list(self._validators)
        validator_list.append(TextClassificationValidator(
            app_label=self.model._meta.app_label,
            model=self.model._meta.model_name,
            field_name=self.name,
        ))
        return validator_list
