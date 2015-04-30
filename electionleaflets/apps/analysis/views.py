import datetime

from django.views.generic import TemplateView, RedirectView
from django.db.models import Count
from django.contrib.auth.models import User

from .models import LeafletProperties
from constituencies.models import Constituency
from leaflets.models import Leaflet

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

        context['total_contributions'] = LeafletProperties.objects\
            .leaflets_analysed()

        context['number_of_people'] = LeafletProperties.objects\
                    .order_by().values_list('user').distinct().count()

        context['leaflets_analysed'] = LeafletProperties.objects\
                    .leaflets_analysed()

        context['with_party_leaders'] = LeafletProperties.objects\
                    .leaders_photo_count()

        context['with_graph'] = LeafletProperties.objects\
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

class AnalysisReportView(ReportViewMixin, TemplateView):
    template_name = "analysis/reports/analysis.html"

    def get_context_data(self, **kwargs):
        context = super(AnalysisReportView, self).get_context_data(**kwargs)

        context['leaflet_count'] = self.leaflet_count

        context['leaders_photo_count'] = \
            LeafletProperties.objects.leaders_photo_count()
        context['leaders_mentions'] = \
            LeafletProperties.objects.leaders_photo_count()
        context['party_logo'] = \
            LeafletProperties.objects.party_logo()
        context['opposition_photo_count'] = \
            LeafletProperties.objects.opposition_photo_count()
        context['opposition_mentions_count'] = \
            LeafletProperties.objects.opposition_mentions_count()
        context['squeeze_messages_count'] = \
            LeafletProperties.objects.squeeze_messages_count()
        context['graphs_count'] = \
            LeafletProperties.objects.graphs_count()

        context['type_leaflet_count'] = \
            LeafletProperties.objects.leaflet_type_count('Leaflet')
        context['type_letter_count'] = \
            LeafletProperties.objects.leaflet_type_count('Letter')
        context['type_magazine_count'] = \
            LeafletProperties.objects.leaflet_type_count('Magazine')
        context['type_newsletter_count'] = \
            LeafletProperties.objects.leaflet_type_count('Newsletter')
        context['type_newspaper_count'] = \
            LeafletProperties.objects.leaflet_type_count('Newspaper')
        context['type_cv_count'] = \
            LeafletProperties.objects.leaflet_type_count('CV')
        context['type_survey_count'] = \
            LeafletProperties.objects.leaflet_type_count('Survey')


        return context
