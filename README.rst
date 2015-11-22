django-textclassifier
=====================

Validators and some utility functions for validating fields using a naive
bayesian text classifier, provided by `TextBlob`_

.. _TextBlob: http://textblob.readthedocs.org/

Usage
-----

Add this application to your Django project::

    INSTALLED_APPS = [
        ...
        'textclassifier',
        ...
    ]

You'll also need to set the data file source in your settings::

    TEXTCLASSIFIER_DATA_FILE = '/tmp/test.json'

.. note::
    The current implementation is very basic, only allowing for one data file.
    This will eventually be more configurable, but is just a POC for now.

Data file
---------

The data file needs to be written by hand for now as well. It is read using the
`TextBlob JSON formatter`_

.. _`TextBlob JSON formatter`: http://textblob.readthedocs.org/en/dev/api_reference.html#textblob.formats.JSON

The file should use the labels ``spam`` and ``valid``::

    [
        {"text": "This is spam", "label": "spam"},
        {"text": "This is valid", "label": "valid"}
    ]
