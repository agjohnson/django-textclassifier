from django.contrib import admin

from textclassifier.admin import (classify_as_spam, classify_as_spam_and_delete,
                                  classify_as_valid)

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    actions = [classify_as_valid, classify_as_spam, classify_as_spam_and_delete]
