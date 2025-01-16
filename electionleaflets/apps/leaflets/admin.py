from copy import deepcopy

from core.helpers import JSONEditor
from django.contrib import admin
from leaflets.models import Leaflet, LeafletImage
from sorl.thumbnail import get_thumbnail

from .admin_widgets import AdminImageMixin


class LeafletImageInline(AdminImageMixin, admin.TabularInline):
    model = LeafletImage


class LeafletAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "ynr_party_name",
        "postcode",
        "name",
        "email",
        "get_description",
        "status",
    ]
    list_filter = [
        "status",
    ]
    exclude = (
        "ynr_party_name",
        "ynr_person_id",
    )

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "postcode",
                    "title",
                    "description",
                    "date_delivered",
                    "status",
                    "reviewed",
                )
            },
        ),
        (
            "Internal data",
            {
                "classes": ("collapse",),
                "fields": (
                    "nuts1",
                    "ballots",
                    "people",
                    "person_ids",
                ),
            },
        ),
    )

    search_fields = ["title", "postcode"]
    ordering = ["title"]
    inlines = [
        LeafletImageInline,
    ]

    def get_description(self, obj):
        if obj.description:
            return obj.description[0:50]
        return ""

    get_description.short_description = "Description"

    def get_form(self, *args, **kwargs):
        self.form = deepcopy(self.form)
        form = super().get_form(*args, **kwargs)

        json_fields = [
            "ballots",
            "people",
            "person_ids",
        ]
        for fieldname in json_fields:
            form.base_fields[
                fieldname
            ].help_text = "This field should only edited in exceptional circumstances and if you know exactly what you're doing"
            form.base_fields[fieldname].widget = JSONEditor()
        return form


class LeafletImageOptions(AdminImageMixin, admin.ModelAdmin):
    list_display = ["id", "get_leaflet_title", "thumbnail"]
    ordering = [
        "-id",
    ]
    raw_id_fields = ["leaflet"]

    def get_leaflet_title(self, obj):
        if obj.leaflet:
            return obj.leaflet.title
        return ""

    get_leaflet_title.short_description = "Leaflet title"

    def thumbnail(self, obj):
        if not obj.image:
            return None
        thumb = get_thumbnail(obj.image, "100x100", crop="center")
        return "<img src='%s'>" % thumb.url

    thumbnail.allow_tags = True


admin.site.register(LeafletImage, LeafletImageOptions)
admin.site.register(Leaflet, LeafletAdmin)
