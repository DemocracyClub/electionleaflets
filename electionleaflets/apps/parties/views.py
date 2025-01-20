import re

from django.db.models import Count, Q
from django.http import Http404
from django.views.generic import ListView
from django_filters.views import FilterView
from leaflets.filters import LeafletFilter
from leaflets.models import Leaflet


class PartyList(ListView):
    def get_queryset(self):
        return (
            Leaflet.objects.exclude(ynr_party_id__in=[None, ""])
            .values("ynr_party_id", "ynr_party_name")
            .annotate(count=Count("ynr_party_id"))
            .exclude(count=0)
            .order_by("-count")
        )

    template_name = "parties/party_list.html"


class PartyView(FilterView):
    filterset_class = LeafletFilter
    model = Leaflet
    paginate_by = 60

    def get_queryset(self):
        id = re.sub(r"[^0-9]", "", self.kwargs["pk"])
        return Leaflet.objects.prefetch_related("images").filter(
            Q(ynr_party_id=self.kwargs["pk"]) | Q(ynr_party_id=f"party:{id}")
        )

    def get_context_data(self, **kwargs):
        context = super(PartyView, self).get_context_data(**kwargs)

        if not self.get_queryset().exists():
            raise Http404()

        context["party_name"] = self.get_queryset().first().ynr_party_name

        return context

    template_name = "parties/party_detail.html"
