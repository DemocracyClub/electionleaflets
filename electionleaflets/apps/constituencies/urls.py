from constituencies.views import ConstituencyList, ConstituencyView
from django.urls import re_path
from django.views.decorators.cache import cache_page

urlpatterns = [
    re_path(
        r"^$",
        cache_page(60 * 60)(ConstituencyList.as_view()),
        name="constituencies",
    ),
    re_path(
        r"^(?P<pk>[^/]+)(?:/(?P<ignored_slug>.*))?$",
        ConstituencyView.as_view(),
        name="constituency-view",
    ),
]
