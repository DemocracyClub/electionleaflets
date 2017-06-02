from django.conf.urls import patterns, include, handler500, url
from django.conf import settings
from django.views.decorators.cache import cache_page

from constituencies.views import ConstituencyList, ConstituencyView

urlpatterns = [
    url(r'^$', cache_page(60 * 60)(ConstituencyList.as_view()),
        name='constituencies'),
    url(r'^(?P<pk>[^/]+)(?:/(?P<ignored_slug>.*))?$',
        ConstituencyView.as_view(),
        name='constituency-view'),
]
