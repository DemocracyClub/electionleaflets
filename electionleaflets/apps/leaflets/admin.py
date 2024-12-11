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
        "election",
        "ynr_party_name",
        "constituency",
        "ynr_person_id",
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
