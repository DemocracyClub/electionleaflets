import re

from django.db.models import Q
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from leaflets.models import Leaflet
from .serializers import LeafletSerializer


class StandardResultsSetPagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 1000


class LeafletFilter(filters.FilterSet):
    class Meta:
        model = Leaflet
        fields = ["date_uploaded"]

    def ballot_filter(self, queryset, name, value):
        return queryset.filter(ballots__contains=[{"ballot_paper_id": value}])

    def party_filter(self, queryset, name, value):
        id = re.sub(r"[^0-9]", "", value)

        return queryset.filter(
            Q(publisher_party=value)
            | Q(ynr_party_id=value)
            | Q(ynr_party_id=f"party:{id}")
        )

    ballot = filters.CharFilter(
        field_name="ballots", method="ballot_filter", label="Ballot paper ID"
    )
    party = filters.CharFilter(
        field_name="party", method="party_filter", label="Party ID"
    )


class LeafletViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Leaflet.objects.all().prefetch_related("images")
    serializer_class = LeafletSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LeafletFilter
