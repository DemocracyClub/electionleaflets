from django.contrib import admin
from content.models import ContentBlock


class ContentBlockOptions(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name', 'content']
    ordering = ['name']


admin.site.register(ContentBlock, ContentBlockOptions)
