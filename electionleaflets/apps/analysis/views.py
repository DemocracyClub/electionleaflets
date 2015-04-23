import datetime

from django.views.generic import TemplateView
from django.db.models import Count

from constituencies.models import Constituency
from leaflets.models import Leaflet

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