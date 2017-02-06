"""Classifier database storage"""

from django.db import models


class TrainingData(models.Model):

    class Meta:
        verbose_name_plural = 'training data'

    field = models.CharField(max_length=128)
    data = models.TextField(blank=True, null=True)
