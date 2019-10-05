from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

admin.autodiscover()

from api import feeds  # noqa: E402
from core.views import HomeView, MaintenanceView, ReportView, ReportThanksView, TestView  # noqa: E402

MAINTENANCE_MODE = getattr(settings, 'MAINTENANCE_MODE', False)
if MAINTENANCE_MODE:
    urlpatterns = [
        url(r'.*', MaintenanceView.as_view(), name='maintenance_view'),
    ]

else:
    urlpatterns = [
        url(r'^$', cache_page(60 * 5)(HomeView.as_view()), name='home'),
        url(r'^leaflets/', include('leaflets.urls')),
        url(r'^parties/', include('parties.urls')),
        url(r'^person/', include('people.urls')),
        url(r'^constituencies/', include('constituencies.urls')),
        url(r'^analysis/', include('analysis.urls')),
        url(r'^api/', include('api.urls')),

        # Feeds
        url(r'^feeds/latest/$', feeds.LatestLeafletsFeed(), name='latest_feed'),
        url(r'^feeds/constituency/(?P<cons_slug>[\w_\-\.]+)/$', feeds.ConstituencyFeed(), name='constituency_feed'),

        # Individual urls
        url(r'^about/$', TemplateView.as_view(template_name='core/about.html'), name='about'),
        url(r'^donate/$', TemplateView.as_view(template_name='core/donate.html'), name='donate'),
        url(r'^press/$', TemplateView.as_view(template_name='core/press.html'), name='press'),
        url(r'^report/(?P<pk>\d+)/sent/$', ReportThanksView.as_view(), name='report_abuse_sent'),
        url(r'^report/(?P<pk>\d+)/$', ReportView.as_view(), name='report_abuse'),

        # Administration URLS
        url(r'^admin/', include(admin.site.urls)),
        url(r'^accounts/', include('allauth.urls')),

        url(r'^dc_base_theme', include('dc_theme.urls')),
        url(r'^test', TestView.as_view(), name="test"),
    ]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
