from constituencies.models import Constituency
from django.contrib import admin


class ConstituencyOptions(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
    ]
    search_fields = ["name"]
    ordering = ["name"]


class ConstituencyTypeOptions(admin.ModelAdmin):
    list_display = ["name", "country"]
    search_fields = ["name"]


admin.site.register(Constituency, ConstituencyOptions)
