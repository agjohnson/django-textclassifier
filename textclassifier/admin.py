"""Classifier admin actions"""

from django.contrib import admin

from .models import TrainingData


def classify_as_spam(modeladmin, request, queryset):
    # TODO make this cycle through fields to find classifier fields
    pass


classify_as_spam.short_description = 'Classify object as spam'


def classify_as_spam_and_delete(modeladmin, request, queryset):
    classify_as_spam(modeladmin, request, queryset)
    queryset.delete()


classify_as_spam_and_delete.short_description = 'Classify object as spam and delete'


@admin.register(TrainingData)
class TrainingDataAdmin(admin.ModelAdmin):
    pass
