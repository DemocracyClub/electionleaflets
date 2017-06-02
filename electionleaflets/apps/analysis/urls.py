from django.conf.urls import patterns, include, handler500, url
from django.conf import settings
from django.views.decorators.cache import cache_page


from .views import (AnalysisHomeView, AnalysisReportView, ReportView,
                    AnalysisStartRedirectView, AnalysisPerPartyReportView,
                    ConstituencyReportView)

urlpatterns = [
    url(r'^$', AnalysisHomeView.as_view(),
        name='analysis'),

    url(r'^start/$', AnalysisStartRedirectView.as_view(),
        name='analysis_start'),

    url(r'^reports/constituencies/$',
        cache_page(60 * 5)(ConstituencyReportView.as_view()),
        name='constituencies_report'),

    url(r'^reports/analysis/$',
        cache_page(60 * 5)(AnalysisReportView.as_view()),
        name='analysis_report'),

    url(r'^reports/analysis/per_party/$',
        cache_page(60 * 5)(AnalysisPerPartyReportView.as_view()),
        name='analysis_report_per_party'),

    url(r'^reports/$',
        cache_page(60 * 5)(ReportView.as_view()),
        name='report_view'),
]
