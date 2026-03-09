from copy import deepcopy

from core.helpers import JSONEditor
from django.contrib import admin, messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import path
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

    change_form_template = "admin/leaflets/leaflet/change_form.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:leaflet_id>/rebuild-thumbnails/",
                self.admin_site.admin_view(self.rebuild_thumbnails_view),
                name="leaflets_leaflet_rebuild_thumbnails",
            ),
        ]
        return custom_urls + urls

    def rebuild_thumbnails_view(self, request, leaflet_id):
        leaflet = get_object_or_404(Leaflet, pk=leaflet_id)
        deleted_count = leaflet.clear_thumbs()
        self.message_user(
            request,
            f"Deleted {deleted_count} thumb file(s), leaving the thumbs Lambda to re-make them",
            messages.SUCCESS,
        )
        return redirect("admin:leaflets_leaflet_change", leaflet_id)

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
