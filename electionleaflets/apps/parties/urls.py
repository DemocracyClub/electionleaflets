from django.conf.urls import patterns, url

from parties.views import PartyList, PartyView

urlpatterns = patterns(
    '',
    url(r'^/$',      PartyList.as_view(), name='parties'),
    # url(r'^/(?P<slug>[\w_\-\.]+)/$',  Party.as_view(), name='party'),
    url(r'^/(?P<pk>[^/]+)(?:/(?P<ignored_slug>.*))?$',
            PartyView.as_view(),
            name='party-view'),
)
