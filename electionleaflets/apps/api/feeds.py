# -*- coding: utf-8 -*-

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
