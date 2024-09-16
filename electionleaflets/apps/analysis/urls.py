from django.urls import re_path
from django.views.decorators.cache import cache_page

from .views import (AnalysisHomeView, AnalysisPerPartyReportView,
                    AnalysisReportView, AnalysisStartRedirectView,
                    ConstituencyReportView, NoCandidatesView, ReportView,
                    TagRandomCandidate)

urlpatterns = [
    re_path(r"^$", AnalysisHomeView.as_view(), name="analysis"),
    re_path(
        r"^start/$", AnalysisStartRedirectView.as_view(), name="analysis_start"
    ),
    re_path(
        r"^tag_candidates/$",
        TagRandomCandidate.as_view(),
        name="analysis_tag_random_candidate",
    ),
    re_path(
        r"^reports/constituencies/$",
        cache_page(60 * 5)(ConstituencyReportView.as_view()),
        name="constituencies_report",
    ),
    re_path(
        r"^reports/analysis/$",
        cache_page(60 * 5)(AnalysisReportView.as_view()),
        name="analysis_report",
    ),
    re_path(
        r"^reports/analysis/per_party/$",
        cache_page(60 * 5)(AnalysisPerPartyReportView.as_view()),
        name="analysis_report_per_party",
    ),
    re_path(
        r"^reports/$",
        cache_page(60 * 5)(ReportView.as_view()),
        name="report_view",
    ),
    re_path(
        r"^leaflets_without_candidates/$",
        NoCandidatesView.as_view(),
        name="leaflets_without_candidates",
    ),
]
