"""Test models"""

from django.db import models

from textclassifier.fields import TextClassificationField


class Foobar(models.Model):

    foo = TextClassificationField()
    bar = TextClassificationField()
