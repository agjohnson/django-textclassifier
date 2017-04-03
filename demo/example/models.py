from django.db import models

from textclassifier.fields import TextClassificationField


class Comment(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    subject = models.TextField()
    comment = TextClassificationField()
