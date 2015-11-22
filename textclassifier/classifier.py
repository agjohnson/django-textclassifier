"""Classifier for validation"""

import json

from django.conf import settings

from textblob.classifiers import NaiveBayesClassifier

TEXTCLASSIFIER_DATA_FILE = getattr(settings, 'TEXTCLASSIFIER_DATA_FILE', None)


class DefaultClassifier(NaiveBayesClassifier):
    """Classifier that opens default file based on settings

    This extends :py:cls:`NaiveBayesClassifier` and opens a file found at the
    setting :py:data:`TEXTCLASSIFIER_DATA_FILE`.
    """

    def __init__(self, *args, **kwargs):
        if TEXTCLASSIFIER_DATA_FILE is None:
            raise ValueError('Classifier data file is not set')
        self.data_handle = open(TEXTCLASSIFIER_DATA_FILE, 'r')
        kwargs['format'] = 'json'
        NaiveBayesClassifier.__init__(self, self.data_handle, *args, **kwargs)


class DefaultWriteableClassifier(DefaultClassifier):
    """Writeable version of :py:cls:`DefaultClassifier`"""

    def save(self):
        with open(TEXTCLASSIFIER_DATA_FILE, 'w+') as h:
            data = [{'text': text, 'label': label}
                    for (text, label) in self.train_set]
            json.dump(data, h)
