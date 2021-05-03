from django.conf.urls import url
from django.views.decorators.cache import cache_page


from .views import (
    AnalysisHomeView,
    AnalysisReportView,
    ReportView,
    AnalysisStartRedirectView,
    AnalysisPerPartyReportView,
    ConstituencyReportView,
    CandidateTagging,
    TagRandomCandidate, NoCandidatesView,
)

urlpatterns = [
    url(r"^$", AnalysisHomeView.as_view(), name="analysis"),
    url(
        r"^start/$", AnalysisStartRedirectView.as_view(), name="analysis_start"
    ),
    url(
        r"^tag_candidates/$",
        TagRandomCandidate.as_view(),
        name="analysis_tag_random_candidate",
    ),
    url(
        r"^tag_candidates/(?P<leaflet_id>\d+)$",
        CandidateTagging.as_view(),
        name="analysis_tag_candidate",
    ),
    url(
        r"^reports/constituencies/$",
        cache_page(60 * 5)(ConstituencyReportView.as_view()),
        name="constituencies_report",
    ),
    url(
        r"^reports/analysis/$",
        cache_page(60 * 5)(AnalysisReportView.as_view()),
        name="analysis_report",
    ),
    url(
        r"^reports/analysis/per_party/$",
        cache_page(60 * 5)(AnalysisPerPartyReportView.as_view()),
        name="analysis_report_per_party",
    ),
    url(
        r"^reports/$",
        cache_page(60 * 5)(ReportView.as_view()),
        name="report_view",
    ),
    url(
        r"^leaflets_without_candidates/$",
        NoCandidatesView.as_view(),
        name="leaflets_without_candidates",
    ),
]
