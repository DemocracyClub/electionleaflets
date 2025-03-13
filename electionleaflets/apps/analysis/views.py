from django_filters.views import FilterView
from leaflets.filters import LeafletFilter
from leaflets.models import Leaflet


class BaseTagLeafletList(FilterView):
    template_name = "analysis/tag_leaflets.html"
    filterset_class = LeafletFilter
    paginate_by = 30


class WithoutPeopleTagLeafletList(BaseTagLeafletList):
    def get_queryset(self):
        return (
            Leaflet.objects.all()
            .filter(person_ids=[])
            .order_by("-date_uploaded")
        )


class WithoutPartyTagLeafletList(BaseTagLeafletList):
    def get_queryset(self):
        return (
            Leaflet.objects.all()
            .filter(ynr_party_id="")
            .order_by("-date_uploaded")
        )
