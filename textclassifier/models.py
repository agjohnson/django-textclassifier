"""Classifier database storage"""

from django.db import models
from django.utils.translation import ugettext as _


class TrainingData(models.Model):
    """Model for per-field training data"""

    class Meta(object):
        verbose_name_plural = 'training data'
        unique_together = (('app_label', 'model', 'field_name'),)

    app_label = models.CharField(_('Application name'), max_length=100)
    model = models.CharField(_('Model class name'), max_length=100)
    field_name = models.CharField(_('Field name'), max_length=100)

    data = models.TextField(_('Training data'), blank=True, null=True)

    create_date = models.DateTimeField(_('Creation date'), auto_now_add=True)
    update_date = models.DateTimeField(_('Last modification date'), auto_now=True)

    def __unicode__(self):
        return 'For {0}.{1}.{2}'.format(self.app_label, self.model, self.field_name)
