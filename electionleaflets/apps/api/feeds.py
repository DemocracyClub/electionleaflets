# -*- coding: utf-8 -*-
import mimetypes

# from parties.models import Party
from constituencies.models import Constituency
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from leaflets.models import Leaflet


class LatestLeafletsFeed(Feed):
    title = "electionleaflets.org latest items"
    link = "/leaflets/"
    description = "The most recently uploaded leaflets"

    def items(self):
        return Leaflet.objects.order_by("-id")[:100]

    def item_title(self, item):
        return item.get_title()

    def item_description(self, item):
        d = ""
        if item.description:
            d = item.description
        if item.images.all():
            d = "{0} – {1}".format(d, item.images.all()[0].image.url)
        return d

    def item_enclosure_url(self, item):
        if item.images.all():
            return item.images.all()[0].image.url
        return None

    def item_enclosure_length(self, item):
        if item.images.all():
            try:
                return item.images.all()[0].image.size
            except Exception:
                return None
        return None

    def item_enclosure_mime_type(self, item):
        if item.images.all():
            im_type, _ = mimetypes.guess_type(item.images.all()[0].image.url)
            return im_type
        return None


# class PartyFeed(Feed):
#     title = "electionleaflets.org latest party leaflets"
#     description = "The most recently uploaded party leaflets"
#
#     def get_object(self, request, party_slug):
#         obj = get_object_or_404(Party, slug=party_slug)
#         self.link = "/parties/%s/" % obj.slug
#         return obj
#
#     def items(self,obj):
#         return Leaflet.objects.filter(publisher_party=obj).order_by('-id')[:10]
#
#     def item_title(self, item):
#         return item.title
#
#     def item_description(self, item):
#         return item.description


class ConstituencyFeed(Feed):
    def get_object(self, request, cons_slug):
        obj = get_object_or_404(Constituency, slug=cons_slug)
        self.link = "/constituencies/%s/" % obj.slug
        self.description = (
            "The most recently uploaded leaflets for %s" % obj.name
        )
        self.title = "electionleaflets feed for %s" % obj.name
        return obj

    def items(self, obj):
        return Leaflet.objects.filter(constituency=obj).order_by("-id")[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description
