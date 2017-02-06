"""Classifier for validation

These classifier classes extend :py:cls:`NaiveBayesClassifier`, providing
alternative storage mechanisms for the training data.
"""

import json

from django.conf import settings

from textblob.classifiers import NaiveBayesClassifier

from textclassifier.models import TrainingData


class ClassifierStorage(object):

    classifier_class = NaiveBayesClassifier

    def load(self):
        pass

    def save(self):
        pass


class FileStorage(ClassifierStorage):
    """Classifier that uses file storage for a single source"""

    def __init__(self, filename=None):
        if filename is None:
            filename = getattr(settings, 'TEXTCLASSIFIER_DATA_FILE')
        self.filename = filename

    def load(self):
        try:
            handle = open(self.filename, 'r')
            data = json.load(handle)
        except IOError:
            raise IOError('The classification file cannot be opened for reading')
        except ValueError:
            raise ValueError('The classification file is not valid JSON')
        self.classifier = self.classifier_class(data)
        return self.classifier

    def save(self):
        try:
            handle = open(self.filename, 'w+')
            data = [{'text': text, 'label': label}
                    for (text, label) in self.classifier.train_set]
            json.dump(data, handle)
        except IOError:
            raise IOError('The classification file cannot be opened for writing')


class DatabaseStorage(ClassifierStorage):
    """Classifier that uses database modeling to store classification per-field"""

    def __init__(self, field_name):
        self.field_name = field_name

    def load(self):
        try:
            data_obj = TrainingData.objects.get(field=self.field_name)
            data = json.loads(data_obj.data)
        except (TrainingData.DoesNotExist, TypeError):
            data = {}
        except ValueError:
            raise ValueError('The classification data for "%s" is not valid JSON',
                             self.field_name)
        self.classifier = self.classifier_class(data)
        return self.classifier

    def save(self):
        data = json.dumps([{'text': text, 'label': label}
                           for (text, label) in self.classifier.train_set])
        try:
            (TrainingData.objects
             .filter(field=self.field_name)
             .update(data=data))
        except TrainingData.DoesNotExist:
            TrainingData.objects.create(field=self.field_name, data=data)
