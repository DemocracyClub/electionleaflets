from datetime import datetime
import re

from django.http import Http404
from django.views.generic import DetailView, ListView
from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from uk_political_parties.models import Party
from leaflets.models import Leaflet


class PartyList(ListView):
    def get_queryset(self):

        queryset = Party.objects.annotate(
            num_leaflets=Count("leaflet")
        ).order_by("-num_leaflets", "party_name")
        return queryset

    template_name = "parties/party_list.html"


class PartyView(DetailView):
    model = Party

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        if self.kwargs["pk"].startswith("ynmp"):
            fixed_id = self.kwargs["pk"]
        else:
            fixed_id = "PP" + re.sub(r"[^0-9]", "", self.kwargs["pk"])
        queryset = queryset.filter(
            Q(party_id=self.kwargs["pk"]) | Q(party_id=fixed_id)
        )
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                "No %(verbose_name)s found matching the query"
                % {"verbose_name": queryset.model._meta.verbose_name}
            )
        return obj

    def get_context_data(self, **kwargs):
        context = super(PartyView, self).get_context_data(**kwargs)
        id = re.sub(r"[^0-9]", "", self.kwargs["pk"])
        qs = Leaflet.objects.filter(
            Q(publisher_party=self.kwargs["pk"])
            | Q(ynr_party_id=self.kwargs["pk"])
            | Q(ynr_party_id=f"party:{id}")
        )

        paginator = Paginator(qs, 60)
        page = self.request.GET.get("page")

        if not page or page == 1:
            if qs:
                context["last_leaflet_days"] = (
                    datetime.now() - qs[0].date_uploaded
                ).days

        try:
            context["party_leaflets"] = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            context["party_leaflets"] = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            context["party_leaflets"] = paginator.page(paginator.num_pages)

        return context

    template_name = "parties/party_detail.html"
