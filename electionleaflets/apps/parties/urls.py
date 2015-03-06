from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page

from parties.views import PartyList, PartyView

urlpatterns = patterns(
    '',
    url(r'^/$',      cache_page(60*60)(PartyList.as_view()), name='parties'),
    # url(r'^/(?P<slug>[\w_\-\.]+)/$',  Party.as_view(), name='party'),
    url(r'^/(?P<pk>[^/]+)(?:/(?P<ignored_slug>.*))?$',
            PartyView.as_view(),
            name='party-view'),
)
