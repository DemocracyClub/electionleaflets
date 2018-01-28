from django.contrib import admin
from tags.models import Tag


class TagOptions(admin.ModelAdmin):
    list_display = ['tag', 'tag_clean', 'slug', 'dead']
    list_filter = ('dead',)
    search_fields = ['tag']
    ordering = ['tag']


admin.site.register(Tag, TagOptions)
