import datetime

from django.contrib import messages
from django.urls import reverse
from django.views.generic import TemplateView, RedirectView, UpdateView
from django.db.models import Count
from django.contrib.auth.models import User

from analysis.forms import CandidateTaggerForm
from core.helpers import CacheControlMixin
from .models import LeafletProperties
from constituencies.models import Constituency
from leaflets.models import Leaflet, devs_dc_helper
from uk_political_parties.models import Party


class AnalysisHomeView(TemplateView):
    template_name = "analysis/index.html"

    def get_context_data(self, **kwargs):
        context = super(AnalysisHomeView, self).get_context_data(**kwargs)

        context["contributing_people"] = (
            User.objects.exclude(leafletproperties=None)
            .annotate(
                edits_count=Count("leafletproperties__leaflet", distinct=True)
            )
            .order_by("-edits_count")[:10]
        )

        context[
            "total_contributions"
        ] = LeafletProperties.objects.all().leaflets_analysed()

        context["number_of_people"] = (
            LeafletProperties.objects.order_by()
            .values_list("user")
            .distinct()
            .count()
        )

        context[
            "leaflets_analysed"
        ] = LeafletProperties.objects.all().leaflets_analysed()

        context[
            "with_party_leaders"
        ] = LeafletProperties.objects.all().leaders_photo_count()

        context["with_graph"] = LeafletProperties.objects.all().graphs_count()

        return context


class AnalysisStartRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        start_date = datetime.date(2015, 1, 1)
        next_leaflet = (
            Leaflet.objects.filter(leafletproperties=None)
            .filter(date_uploaded__gt=start_date)
            .order_by("?")
        )
        url = next_leaflet[0].get_absolute_url()
        return url


class ReportViewMixin(object):
    @property
    def leaflet_count(self):
        start_date = datetime.date(2015, 1, 1)
        return Leaflet.objects.filter(date_uploaded__gt=start_date).count()


class ReportView(ReportViewMixin, TemplateView):
    template_name = "analysis/reports/index.html"

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data(**kwargs)
        start_date = datetime.date(2015, 1, 1)
        context["start_date"] = start_date

        # Get leaflet count
        context["leaflet_count"] = self.leaflet_count

        return context


class ConstituencyReportView(ReportViewMixin, TemplateView):
    template_name = "analysis/reports/constituencies.html"

    def get_context_data(self, **kwargs):
        context = super(ConstituencyReportView, self).get_context_data(**kwargs)

        # Get per constituency
        per_constituency = (
            Constituency.objects.filter(
                leaflet__date_uploaded__gt=datetime.date(2015, 1, 1)
            )
            .annotate(leaflets_count=Count("leaflet"))
            .order_by("-leaflets_count")
        )
        context["per_constituency"] = per_constituency

        return context


class BaseAnalysisReportView(ReportViewMixin, TemplateView):
    def add_data_to_context(self, queryset=None):
        if not queryset:
            queryset = self.base_queryset

        context = {}
        context["leaflet_count"] = self.leaflet_count

        context["leaders_photo_count"] = queryset.leaders_photo_count()
        context["leaders_mentions"] = queryset.leaders_mentions()
        context["party_logo"] = queryset.party_logo()
        context["opposition_photo_count"] = queryset.opposition_photo_count()
        context[
            "opposition_mentions_count"
        ] = queryset.opposition_mentions_count()
        context["squeeze_messages_count"] = queryset.squeeze_messages_count()
        context["graphs_count"] = queryset.graphs_count()

        context["type_leaflet_count"] = queryset.leaflet_type_count("Leaflet")
        context["type_letter_count"] = queryset.leaflet_type_count("Letter")
        context["type_magazine_count"] = queryset.leaflet_type_count("Magazine")
        context["type_newsletter_count"] = queryset.leaflet_type_count(
            "Newsletter"
        )
        context["type_newspaper_count"] = queryset.leaflet_type_count(
            "Newspaper"
        )
        context["type_cv_count"] = queryset.leaflet_type_count("CV")
        context["type_survey_count"] = queryset.leaflet_type_count("Survey")

        return context


class AnalysisReportView(BaseAnalysisReportView):
    template_name = "analysis/reports/analysis.html"
    base_queryset = LeafletProperties.objects.all()

    def get_context_data(self, **kwargs):
        context = super(AnalysisReportView, self).get_context_data(**kwargs)
        context.update(self.add_data_to_context())
        return context


class AnalysisPerPartyReportView(BaseAnalysisReportView):
    template_name = "analysis/reports/analysis_per_party.html"
    base_queryset = LeafletProperties.objects.all()

    def get_context_data(self, **kwargs):
        context = super(AnalysisPerPartyReportView, self).get_context_data(
            **kwargs
        )
        parties = []
        for party in Party.objects.filter(
            leaflet__date_uploaded__gte=datetime.date(2015, 1, 1)
        ).distinct():
            qs = LeafletProperties.objects.filter(
                leaflet__publisher_party_id=party.pk
            )

            if qs:
                parties.append(
                    {
                        "party": party,
                        "data": self.add_data_to_context(queryset=qs),
                    }
                )

        context["parties"] = parties
        return context


class BaseCandidateTaggingMixin:
    def get_queryset(self):
        last_30_days = datetime.datetime.now() - datetime.timedelta(days=30)
        qs = (
            Leaflet.objects.exclude(postcode="")
            .filter(publisher_person=None)
            .filter(date_uploaded__gte=last_30_days)
        )
        return qs


class TagRandomCandidate(BaseCandidateTaggingMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        qs = self.get_queryset()
        if qs.exists():
            leaflet = self.get_queryset().order_by("?").first()
            return reverse(
                "analysis_tag_candidate", kwargs={"leaflet_id": leaflet.pk}
            )
        else:
            messages.success(self.request, "No more candidates lift to tag!")
            return reverse("analysis")


class CandidateTagging(UpdateView):
    pk_url_kwarg = "leaflet_id"
    model = Leaflet
    form_class = CandidateTaggerForm
    template_name = "analysis/candidate_tagging.html"

    def get_initial(self):
        postcode_results = devs_dc_helper.postcode_request(
            postcode=self.object.postcode
        )
        return {"postcode_results": postcode_results}

    def form_valid(self, form):

        messages.success(self.request, "Thanks for tagging that candidate!")
        return super(CandidateTagging, self).form_valid(form)

    def get_success_url(self):

        return reverse("analysis_tag_random_candidate")


class NoCandidatesView(CacheControlMixin, TemplateView):
    cache_timeout = 0
    template_name = "analysis/no_candidates.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Leaflet.objects.filter(
            people__iexact="{}"
        )
        if self.request.GET.get("existing"):
            qs = qs.exclude(ynr_person_id=None)
        context["leaflets"] = qs.order_by("-date_uploaded")[:10]
        return context
