"""Test models"""

from django.db import models

from textclassifier.fields import ClassifierTextField


class Foobar(models.Model):

    foo = ClassifierTextField()
    bar = ClassifierTextField()
