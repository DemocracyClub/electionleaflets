from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

admin.autodiscover()

from api import feeds

from core.views import HomeView, MaintenanceView, ReportView, ReportThanksView
MAINTENANCE_MODE = getattr(settings, 'MAINTENANCE_MODE', False)
if MAINTENANCE_MODE:
    urlpatterns = patterns(
        '',
        url(r'.*', MaintenanceView.as_view(), name='maintenance_view'),
    )

else:
    urlpatterns = patterns(
        '',

        url(r'^$',          cache_page(60*5)(HomeView.as_view()), name='home'),
        url(r'^leaflets',   include('leaflets.urls')),
        url(r'^parties',    include('parties.urls')),
        url(r'^constituencies',    include('constituencies.urls')),
        url(r'^analysis',   include('analysis.urls')),
        url(r'^tags',       include('tags.urls')),
        url(r'^categories', include('categories.urls')),
        url(r'^api/', include('api.urls')),

        # Feeds
        url(r'^feeds/latest/$', feeds.LatestLeafletsFeed(), name='latest_feed'),
        url(r'^feeds/constituency/(?P<cons_slug>[\w_\-\.]+)/$', feeds.ConstituencyFeed(), name='constituency_feed'),
        url(r'^feeds/category/(?P<cat_slug>[\w_\-\.]+)/$', feeds.CategoryFeed(), name='category_feed'),
        url(r'^feeds/tag/(?P<tag_slug>[\w_\-\.]+)/$', feeds.TagFeed(), name='tag_feed'),

        # Individual urls
        url(r'^about/$', TemplateView.as_view(template_name='core/about.html'), name='about'),
        url(r'^donate/$', TemplateView.as_view(template_name='core/donate.html'), name='donate'),
        url(r'^report/(?P<pk>\d+)/sent/$', ReportThanksView.as_view(), name='report_abuse_sent'),
        url(r'^report/(?P<pk>\d+)/$', ReportView.as_view(), name='report_abuse'),

        # Administration URLS
        (r'^admin/', include(admin.site.urls)),
        url(r'^accounts/', include('allauth.urls')),
    )

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)