# -*- coding: utf-8 -*-

# from parties.models import Party
from django.contrib.syndication.views import Feed
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
