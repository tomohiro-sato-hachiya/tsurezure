from django.contrib import admin
from . import models
from markdownx.admin import MarkdownxModelAdmin

admin.site.register(models.UserExpansion)
admin.site.register(models.Article, MarkdownxModelAdmin)
admin.site.register(models.Comment)
