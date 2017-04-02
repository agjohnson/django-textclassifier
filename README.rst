django-textclassifier
=====================

Validators and some utility functions for validating fields using a naive
bayesian text classifier and feature extraction, provided by `scikit-learn`_.

.. _sklearn: http://scikit-learn.org/

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
            TextClassificationValidator(field_name='app.mymodel.description')
        ])

Or you can use the included ``TextField`` wrapper:

.. code:: python

    from django.db import models
    from textclassifier.fields import TextClassificationField

    class MyModel(models.Model):
        description = TextClassificationField()
