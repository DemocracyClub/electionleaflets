import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, re_path, include
from django.views.generic import TemplateView

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
        re_path(r"^constituencies/", include("constituencies.urls")),
        re_path(r"^analysis/", include("analysis.urls")),
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

urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
