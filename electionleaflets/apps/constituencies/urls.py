from django.conf.urls import patterns, include, handler500, url
from django.conf import settings

from constituencies.views import ConstituencyList, ConstituencyView

urlpatterns = patterns(
    '',
    url(r'^/$',  ConstituencyList.as_view(), name='constituencies'),
    # url(r'^/notspots/', view_not_spots, name='constituency_notspots'),
    url(r'^/(?P<pk>[^/]+)(?:/(?P<ignored_slug>.*))?$',
            ConstituencyView.as_view(),
            name='constituency-view'),
)

