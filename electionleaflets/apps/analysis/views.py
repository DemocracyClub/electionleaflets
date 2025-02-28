from django_filters.views import FilterView
from leaflets.filters import LeafletFilter
from leaflets.models import Leaflet


class TagLeafletList(FilterView):
    template_name = "analysis/tag_leaflets.html"
    filterset_class = LeafletFilter
    paginate_by = 30

    def get_queryset(self):
        qs = Leaflet.objects.all()
        if "/without_party/" in self.request.path:
            qs = qs.filter(ynr_party_id="")
        if "/without_people/" in self.request.path:
            qs = qs.filter(person_ids=[])
        return qs.order_by("-date_uploaded")
