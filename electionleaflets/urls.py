import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, re_path, include
from django.views.generic import TemplateView, RedirectView

from electionleaflets.apps.api.feeds import ConstituencyFeed, LatestLeafletsFeed
from electionleaflets.apps.core.views import HomeView, MaintenanceView, ReportThanksView, ReportView

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
        # Feeds
        re_path(
            r"^feeds/latest/$", LatestLeafletsFeed(), name="latest_feed"
        ),
        re_path(
            r"^feeds/constituency/(?P<cons_slug>[\w_\-\.]+)/$",
            ConstituencyFeed(),
            name="constituency_feed",
        ),
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
        re_path(
            r"^report/(?P<pk>\d+)/sent/$",
            ReportThanksView.as_view(),
            name="report_abuse_sent",
        ),
        re_path(
            r"^report/(?P<pk>\d+)/$", ReportView.as_view(), name="report_abuse"
        ),
        # Administration URLS
        path("admin/", admin.site.urls),
        path('__debug__/', include(debug_toolbar.urls)),
    ]


# Old redirects

class HomePageRedirectView(RedirectView):
    """
    Just redirect to the home page.
    """
    permanent = True
    query_string = True
    pattern_name = "home"


redirect_urls = (
    re_path(r"^analysis", HomePageRedirectView.as_view(), name="analysis"),
    re_path(
        r"^start/$", HomePageRedirectView.as_view(), name="analysis_start"
    ),
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
        r"^leaflets_without_candidates/$",
        HomePageRedirectView.as_view(),
        name="leaflets_without_candidates",
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
)

urlpatterns += redirect_urls

urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
