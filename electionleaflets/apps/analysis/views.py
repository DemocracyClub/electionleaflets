import datetime

from django.views.generic import TemplateView, RedirectView
from django.db.models import Count
from django.contrib.auth.models import User

from .models import LeafletProperties
from constituencies.models import Constituency
from leaflets.models import Leaflet
from uk_political_parties.models import Party

class AnalysisHomeView(TemplateView):
    template_name = "analysis/index.html"

    def get_context_data(self, **kwargs):
        context = super(AnalysisHomeView, self).get_context_data(**kwargs)

        context['contributing_people'] = User.objects\
            .exclude(leafletproperties=None)\
            .annotate(edits_count=Count(
                'leafletproperties__leaflet',
                distinct=True))\
            .order_by('-edits_count')[:10]

        context['total_contributions'] = LeafletProperties.objects.all()\
            .leaflets_analysed()

        context['number_of_people'] = LeafletProperties.objects\
                    .order_by().values_list('user').distinct().count()

        context['leaflets_analysed'] = LeafletProperties.objects.all()\
                    .leaflets_analysed()

        context['with_party_leaders'] = LeafletProperties.objects.all()\
                    .leaders_photo_count()

        context['with_graph'] = LeafletProperties.objects.all()\
                    .graphs_count()


        return context

class AnalysisStartRedirectView(RedirectView):
    permanent = False
    def get_redirect_url(self, *args, **kwargs):
        start_date = datetime.date(2015, 1, 1)
        next_leaflet = Leaflet.objects.filter(leafletproperties=None)\
        .filter(date_uploaded__gt=start_date)\
        .order_by('?')
        url = next_leaflet[0].get_absolute_url()
        return url

class ReportViewMixin(object):
    start_date = datetime.date(2015, 1, 1)
    leaflet_count = Leaflet.objects.filter(
                date_uploaded__gt=start_date).count()

class ReportView(ReportViewMixin, TemplateView):
    template_name = "analysis/reports/index.html"

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data(**kwargs)
        start_date = datetime.date(2015, 1, 1)
        context['start_date'] = start_date

        # Get leaflet count
        context['leaflet_count'] = self.leaflet_count

        return context

class ConstituencyReportView(ReportViewMixin, TemplateView):
    template_name = "analysis/reports/constituencies.html"

    def get_context_data(self, **kwargs):
        context = super(ConstituencyReportView, self).get_context_data(**kwargs)

        # Get per constituency
        per_constituency = Constituency.objects.filter(
            leaflet__date_uploaded__gt=self.start_date).annotate(
            leaflets_count=Count('leaflet')
        ).order_by('-leaflets_count')
        context['per_constituency'] = per_constituency

        return context

class BaseAnalysisReportView(ReportViewMixin, TemplateView):
    def add_data_to_context(self, queryset=None):
        if not queryset:
            queryset = self.base_queryset

        context = {}
        context['leaflet_count'] = self.leaflet_count

        context['leaders_photo_count'] = \
            queryset.leaders_photo_count()
        context['leaders_mentions'] = \
            queryset.leaders_photo_count()
        context['party_logo'] = \
            queryset.party_logo()
        context['opposition_photo_count'] = \
            queryset.opposition_photo_count()
        context['opposition_mentions_count'] = \
            queryset.opposition_mentions_count()
        context['squeeze_messages_count'] = \
            queryset.squeeze_messages_count()
        context['graphs_count'] = \
            queryset.graphs_count()

        context['type_leaflet_count'] = \
            queryset.leaflet_type_count('Leaflet')
        context['type_letter_count'] = \
            queryset.leaflet_type_count('Letter')
        context['type_magazine_count'] = \
            queryset.leaflet_type_count('Magazine')
        context['type_newsletter_count'] = \
            queryset.leaflet_type_count('Newsletter')
        context['type_newspaper_count'] = \
            queryset.leaflet_type_count('Newspaper')
        context['type_cv_count'] = \
            queryset.leaflet_type_count('CV')
        context['type_survey_count'] = \
            queryset.leaflet_type_count('Survey')

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
        context = super(
            AnalysisPerPartyReportView, self).get_context_data(**kwargs)
        parties = []
        for party in Party.objects.filter(
                leaflet__date_uploaded__gte=datetime.date(2015, 1, 1))\
                .distinct():
            qs = LeafletProperties.objects.filter(
                leaflet__publisher_party_id=party.pk)

            parties.append({
                'party': party,
                'data': self.add_data_to_context(queryset=qs),
            })

        context['parties'] = parties
        return context

