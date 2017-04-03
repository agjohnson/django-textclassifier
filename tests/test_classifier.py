# -*- coding: utf-8 -*-

"""Test classifier"""

import os
import sys
import json

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

# First load settings
import mock
from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings

from textclassifier.validators import TextClassificationValidator
from textclassifier.classifier import NaiveBayesClassifier
from textclassifier.models import TrainingData
from textclassifier.constants import VALID, SPAM


class TestClassifier(TestCase):

    def setUp(self):
        self.data = [
            (u'This is not spam', VALID),
            (u'Completely valid field value', VALID),
            (u'Legitimate text that will not fail', VALID),
            (u'', VALID),
            (u'सृजन111 buy viagr@ सृजन', SPAM),
            (u'Buy, Sell and cashing out bitcoins', SPAM),
            (u'Every Sports Game Live On your TV in HD Quality On Your TV Free', SPAM),
            (u'Limited Time Remaining to Renew Your Vehicle Warranty. Warranty No. 9230594', SPAM),
        ]
        self.training_data = TrainingData.objects.create(
            app_label='foo',
            model='bar',
            field_name='foobar',
            data=json.dumps(self.data),
        )

    def test_classifier_classifies(self):
        classifier = NaiveBayesClassifier(
            app_label='foo',
            model='bar',
            field_name='foobar'
        )
        assert classifier.classify('this is not spam').is_valid()
        assert classifier.classify('Buy Your Vehicle Warranty').is_spam()
        assert classifier.classify('BUY YOUR VEHICLE WARRANTY').is_spam()

    def test_classifier_threshold_matters(self):
        classifier = NaiveBayesClassifier(
            app_label='foo',
            model='bar',
            field_name='foobar'
        )
        assert classifier.classify('BUY YOUR VEHICLE WARRANTY').is_spam(0.95)
        assert not classifier.classify('BUY YOUR VEHICLE WARRANTY').is_spam(0.99)

    def test_classifier_unicode_is_classified(self):
        classifier = NaiveBayesClassifier(
            app_label='foo',
            model='bar',
            field_name='foobar'
        )
        assert classifier.classify(u'सृजन सृजन').is_spam(0.6)

    def test_classifier_missing_training_data(self):
        classifier = NaiveBayesClassifier(
            app_label='foo',
            model='bar',
            field_name='not_foobar'
        )
        assert classifier.training_data == []
        assert not classifier.classify('BUY YOUR VEHICLE WARRANTY').is_spam()

    def test_classifier_uses_incomplete_training_data(self):
        training_data = TrainingData.objects.create(
            app_label='foo',
            model='bar',
            field_name='more_foobar',
            data=json.dumps([
                (u'This is spam', SPAM),
                (u'This is not spam', SPAM),
            ]),
        )
        classifier = NaiveBayesClassifier(
            app_label='foo',
            model='bar',
            field_name='more_foobar'
        )
        assert classifier.classify('Nothing').is_spam(0.95)

    def test_classifier_invalid_training_data(self):
        training_data = TrainingData.objects.create(
            app_label='foo',
            model='bar',
            field_name='invalid_data',
            data='null',
        )
        classifier = NaiveBayesClassifier(
            app_label='foo',
            model='bar',
            field_name='invalid_data'
        )
        assert classifier.training_data == []
        assert classifier.classify('Anything').is_valid()

    def test_classifier_saves(self):
        classifier = NaiveBayesClassifier(
            app_label='foo',
            model='bar',
            field_name='previously_empty'
        )
        classifier.update('Lorem ipsum dolor sit amet', VALID)
        assert classifier.training_data == [('Lorem ipsum dolor sit amet', VALID)]
        field = TrainingData.objects.get(
            app_label='foo',
            model='bar',
            field_name='previously_empty'
        )
        assert field.data == '[["Lorem ipsum dolor sit amet", "valid"]]'
