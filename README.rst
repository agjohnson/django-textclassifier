django-textclassifier
=====================

Validators and some utility functions for validating fields using a naive
bayesian text classifier and feature extraction, provided by `scikit-learn`_.

.. image:: https://travis-ci.org/agjohnson/django-textclassifier.svg?branch=master

.. _scikit-learn: http://scikit-learn.org/

Usage
-----

Add this application to your Django project::

    INSTALLED_APPS = [
        ...
        'textclassifier',
        ...
    ]

Model fields can be protected by text classification validation by either
adding the validator to an existing field:

.. code:: python

    from django.db import models
    from textclassifier.validators import TextClassificationValidator

    class MyModel(models.Model):
        description = models.TextField(validators=[
            TextClassificationValidator(
                app_label='app',
                model='mymodel',
                field_name='description'
            )
        ])

Or you can use the included ``TextField`` wrapper:

.. code:: python

    from django.db import models
    from textclassifier.fields import TextClassificationField

    class MyModel(models.Model):
        description = TextClassificationField()

There are also admin action helpers that you can add to your admin model:

.. code:: python

    from textclassifier.admin import classify_as_valid, classify_as_spam, classify_as_spam_and_delete

    @admin.register(MyModel)
    class MyModelAdmin(admin.ModelAdmin):
        actions = [classify_as_valid, classify_as_spam, classify_as_spam_and_delete]
