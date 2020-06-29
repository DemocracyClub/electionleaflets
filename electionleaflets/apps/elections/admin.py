from django.contrib import admin
from elections.models import Election


class ElectionOptions(admin.ModelAdmin):
    list_display = ["name", "country", "active"]
    search_fields = ["name"]
    ordering = ["live_date"]


admin.site.register(Election, ElectionOptions)
