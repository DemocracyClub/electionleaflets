from django.contrib import admin
from core.models import Country, EmailAlert


class CountryOptions(admin.ModelAdmin):
    list_display = ["name", "iso", "iso3"]
    search_fields = ["name"]
    ordering = ["name"]


class EmailAlertOptions(admin.ModelAdmin):
    list_display = ["title", "type"]
    search_fields = ["title"]


admin.site.register(Country, CountryOptions)
admin.site.register(EmailAlert, EmailAlertOptions)
