"""Classifier admin actions"""

from django.contrib import admin

from .classifier import NaiveBayesClassifier
from .constants import SPAM, VALID
from .fields import TextClassificationField
from .models import TrainingData


def classify_queryset(modeladmin, request, queryset, classification=SPAM):
    for obj in queryset:
        for field in obj._meta.fields:
            if isinstance(field, TextClassificationField):
                classifier = NaiveBayesClassifier(
                    app_label=obj._meta.app_label,
                    model=obj._meta.model_name,
                    field_name=field.name
                )
                classifier.update(getattr(obj, field.name), classification)


def classify_as_spam(modeladmin, request, queryset):
    classify_queryset(modeladmin, request, queryset, classification=SPAM)


classify_as_spam.short_description = 'Classify object as spam'


def classify_as_spam_and_delete(modeladmin, request, queryset):
    classify_as_spam(modeladmin, request, queryset, classification=SPAM)
    queryset.delete()


classify_as_spam_and_delete.short_description = 'Classify object as spam and delete'


def classify_as_valid(modeladmin, request, queryset):
    classify_queryset(modeladmin, request, queryset, classification=VALID)


classify_as_valid.short_description = 'Classify object as valid'


@admin.register(TrainingData)
class TrainingDataAdmin(admin.ModelAdmin):
    pass
