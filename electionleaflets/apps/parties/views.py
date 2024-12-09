import re
from datetime import datetime

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, Q
from django.http import Http404
from django.views.generic import ListView, TemplateView
from leaflets.models import Leaflet


class PartyList(ListView):
    def get_queryset(self):
        return (
            Leaflet.objects.exclude(ynr_party_id__in=[None, ""])
            .values("ynr_party_id", "ynr_party_name")
            .annotate(count=Count("ynr_party_id"))
            .order_by("-count")
        )

    template_name = "parties/party_list.html"


class PartyView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(PartyView, self).get_context_data(**kwargs)
        id = re.sub(r"[^0-9]", "", self.kwargs["pk"])
        qs = Leaflet.objects.filter(
            Q(ynr_party_id=self.kwargs["pk"]) | Q(ynr_party_id=f"party:{id}")
        )
        if not qs.exists():
            raise Http404()

        context["party_name"] = qs.first().ynr_party_name

        paginator = Paginator(qs, 60)
        page = self.request.GET.get("page")

        if not page or page == 1 and qs:
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
