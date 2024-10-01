from django.urls import re_path
from django.views.decorators.cache import cache_page
from parties.views import PartyList, PartyView

urlpatterns = [
    re_path(r"^$", cache_page(60 * 60)(PartyList.as_view()), name="parties"),
    re_path(
        r"^(?P<pk>[^/]+)(?:/(?P<ignored_slug>.*))?$",
        PartyView.as_view(),
        name="party-view",
    ),
]
