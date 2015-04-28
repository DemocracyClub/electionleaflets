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

        context['number_of_people'] = LeafletProperties.objects\
                    .order_by().values_list('user').distinct().count()

        context['leaflets_analysed'] = LeafletProperties.objects\
                    .order_by().values_list('leaflet').distinct().count()

        context['with_party_leaders'] = LeafletProperties.objects\
                    .filter(key="has_leader_photo").count()

        context['with_graph'] = LeafletProperties.objects\
                    .filter(key="include_graph", value="Yes").count()


        return context

class AnalysisStartRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        next_leaflet = Leaflet.objects.filter(leafletproperties=None)
        url = next_leaflet[0].get_absolute_url()
        return url


class ReportView(TemplateView):
    template_name = "analysis/reports.html"

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data(**kwargs)
        start_date = datetime.date(2015, 1, 1)
        context['start_date'] = start_date

        # Get leaflet count
        start_date = datetime.date(2015, 1, 1)
        context['leaflet_count'] = Leaflet.objects.filter(
            date_uploaded__gt=start_date).count()

        # Get per constituency
        per_constituency = Constituency.objects.filter(
            leaflet__date_uploaded__gt=start_date).annotate(
            leaflets_count=Count('leaflet')
        ).order_by('-leaflets_count')
        context['per_constituency'] = per_constituency


        return context