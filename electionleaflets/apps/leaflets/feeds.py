from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from leaflets.models import Leaflet
# from parties.models import Party
from constituencies.models import Constituency
from tags.models import Tag
from categories.models import Category

class LatestLeafletsFeed(Feed):
    title = "electionleaflets.org latest items"
    link = "/leaflets/"
    description = "The most recently uploaded leaflets"

    def items(self):
        return Leaflet.objects.order_by('-id')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description


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
        self.link = '/constituencies/%s/' % obj.slug
        self.description = "The most recently uploaded leaflets for %s" % obj.name
        self.title = "electionleaflets feed for %s" % obj.name
        return obj

    def items(self,obj):
        return Leaflet.objects.filter(constituencies=obj).order_by('-id')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

class TagFeed(Feed):

    def get_object(self, request, tag_slug):
        obj = get_object_or_404(Tag, slug=tag_slug)
        self.link = '/tags/%s/' % obj.slug
        self.description = "The most recently uploaded leaflets tagged with %s" % obj.tag
        self.title = "electionleaflets feed for %s" % obj.tag
        return obj

    def items(self,obj):
        return Leaflet.objects.filter(tags=obj).order_by('-id')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description


class CategoryFeed(Feed):

    def get_object(self, request, cat_slug):
        obj = get_object_or_404(Category, slug=cat_slug)
        self.link = '/categories/%s/' % obj.slug
        self.description = "The most recently uploaded leaflets for %s" % obj.name
        self.title = "electionleaflets feed for %s" % obj.name
        return obj

    def items(self,obj):
        return Leaflet.objects.filter(categories=obj).order_by('-id')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

