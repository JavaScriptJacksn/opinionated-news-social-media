from django.contrib import admin
from . import models
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.

@admin.register(models.Post)
class PostAdmin(SummernoteModelAdmin):

    summernote_fields = 'content'

@admin.register(models.Comment)
class CommentAdmin(SummernoteModelAdmin):

    summernote_fields = 'body'
