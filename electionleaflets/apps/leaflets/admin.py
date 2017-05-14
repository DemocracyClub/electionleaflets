from django.contrib import admin
from leaflets.models import Leaflet, LeafletImage

from sorl.thumbnail.admin import AdminImageMixin
from sorl.thumbnail import get_thumbnail


class LeafletImageInline(AdminImageMixin, admin.TabularInline):
    model = LeafletImage


class LeafletAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'publisher_party', 'postcode',
                    'name', 'email', 'get_description', 'status']
    list_filter = ['status', ]
    search_fields = ['title', 'postcode']
    ordering = ['title']
    inlines = [LeafletImageInline, ]

    def get_description(self, obj):
        if obj.description:
            return obj.description[0:50]
        return ''
    get_description.short_description = 'Description'


class LeafletImageOptions(AdminImageMixin, admin.ModelAdmin):
    list_display = ['id', 'get_leaflet_title', 'thumbnail', 'image_text']
    ordering = ['-id', ]
    raw_id_fields = ['leaflet']

    def get_leaflet_title(self, obj):
        if obj.leaflet:
            return obj.leaflet.title
        return ''
    get_leaflet_title.short_description = 'Leaflet title'

    def thumbnail(self, obj):
        if obj.image:
            thumb = get_thumbnail(obj.image, "100x100", crop='center')
            return "<img src='%s'>" % thumb.url
    thumbnail.allow_tags = True

admin.site.register(LeafletImage, LeafletImageOptions)
admin.site.register(Leaflet, LeafletAdmin)
