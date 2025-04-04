from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path, reverse
from django.views.generic import RedirectView, TemplateView

from electionleaflets.apps.api.feeds import LatestLeafletsFeed
from electionleaflets.apps.core.views import (
    HomeView,
    MaintenanceView,
)

admin.autodiscover()

MAINTENANCE_MODE = getattr(settings, "MAINTENANCE_MODE", False)
if MAINTENANCE_MODE:
    urlpatterns = [
        re_path(r".*", MaintenanceView.as_view(), name="maintenance_view"),
    ]

else:
    urlpatterns = [
        re_path(r"^$", HomeView.as_view(), name="home"),
        re_path(r"^leaflets/", include("leaflets.urls")),
        re_path(r"^parties/", include("parties.urls")),
        re_path(r"^person/", include("people.urls")),
        re_path(r"^api/", include("api.urls")),
        re_path(r"^analysis/", include("analysis.urls")),
        # Feeds
        re_path(r"^feeds/latest/$", LatestLeafletsFeed(), name="latest_feed"),
        # Individual urls
        re_path(
            r"^about/$",
            TemplateView.as_view(template_name="core/about.html"),
            name="about",
        ),
        re_path(
            r"^donate/$",
            TemplateView.as_view(template_name="core/donate.html"),
            name="donate",
        ),
        re_path(
            r"^press/$",
            TemplateView.as_view(template_name="core/press.html"),
            name="press",
        ),
        # Administration URLS
        path("admin/", admin.site.urls),
    ]


# Old redirects


class HomePageRedirectView(RedirectView):
    """
    Just redirect to the home page.
    """

    permanent = True
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        return reverse("home")


class RedirectToLeafletView(RedirectView):
    """
    Redirect a URL with a leaflet PK to the canonical URL

    """

    permanent = True
    query_string = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse("leaflet", kwargs={"pk": kwargs["pk"]})


redirect_urls = (
    re_path(r"^analysis", HomePageRedirectView.as_view(), name="analysis"),
    re_path(r"^start/$", HomePageRedirectView.as_view(), name="analysis_start"),
    re_path(
        r"^tag_candidates/$",
        HomePageRedirectView.as_view(),
        name="analysis_tag_random_candidate",
    ),
    re_path(
        r"^reports/constituencies/$",
        HomePageRedirectView.as_view(),
        name="constituencies_report",
    ),
    re_path(
        r"^reports/analysis/$",
        HomePageRedirectView.as_view(),
        name="analysis_report",
    ),
    re_path(
        r"^reports/analysis/per_party/$",
        HomePageRedirectView.as_view(),
        name="analysis_report_per_party",
    ),
    re_path(
        r"^reports/$",
        HomePageRedirectView.as_view(),
        name="report_view",
    ),
    re_path(
        r"^constituencies/$",
        HomePageRedirectView.as_view(),
        name="constituencies",
    ),
    re_path(
        r"^constituencies/(?P<pk>[^/]+)(?:/(?P<ignored_slug>.*))?$",
        HomePageRedirectView.as_view(),
        name="constituency-view",
    ),
    re_path(
        r"^leaflets/(?P<pk>\d+)/images/$",
        RedirectToLeafletView.as_view(),
        name="all_images",
    ),
)

urlpatterns += redirect_urls

urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
