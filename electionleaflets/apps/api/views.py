import re
from datetime import timedelta

from django.db.models import BooleanField, Q
from django.db.models.expressions import RawSQL
from django.utils import timezone
from django_filters import rest_framework as filters
from leaflets.models import Leaflet
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from .serializers import LeafletSerializer


class StandardResultsSetPagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 1000


class LeafletFilter(filters.FilterSet):
    class Meta:
        model = Leaflet
        fields = {"date_uploaded": ["gt", "exact"], "modified": ["gt", "exact"]}

    def ballot_filter(self, queryset, name, value):
        return queryset.filter(ballots__contains=[{"ballot_paper_id": value}])

    def current_filter(self, queryset, name, value):
        current_from = timezone.localdate() - timedelta(days=20)
        is_current = RawSQL(
            """
            EXISTS (
                SELECT 1
                FROM jsonb_array_elements(ballots) AS ballot
                WHERE substring(
                    ballot->>'ballot_paper_id' from '\\d{4}-\\d{2}-\\d{2}$'
                )::date >= %s
            )
            """,
            (current_from,),
            output_field=BooleanField(),
        )

        return (
            queryset.filter(
                Q(date_uploaded__gte=timezone.now() - timedelta(days=180))
            )
            .annotate(is_current=is_current)
            .filter(is_current=value)
        )

    def party_filter(self, queryset, name, value):
        id = re.sub(r"[^0-9]", "", value)

        return queryset.filter(
            Q(ynr_party_id=value) | Q(ynr_party_id=f"party:{id}")
        )

    ballot = filters.CharFilter(
        field_name="ballots", method="ballot_filter", label="Ballot paper ID"
    )
    current = filters.BooleanFilter(method="current_filter", label="Current")
    party = filters.CharFilter(
        field_name="party", method="party_filter", label="Party ID"
    )


class LeafletViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Leaflet.objects.all().prefetch_related("images")
    serializer_class = LeafletSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LeafletFilter
