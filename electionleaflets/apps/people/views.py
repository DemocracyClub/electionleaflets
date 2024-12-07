from datetime import datetime

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import DetailView, TemplateView
from leaflets.models import Leaflet


class PersonView(TemplateView):
    template_name = "people/person.html"

    def get_context_data(self, **kwargs):
        context = super(PersonView, self).get_context_data(**kwargs)
        qs = Leaflet.objects.filter(people__in=self.kwargs["person_id"])

        paginator = Paginator(qs, 60)
        page = self.request.GET.get("page")

        if not page or page == 1 and qs:
            context["last_leaflet_days"] = (
                datetime.now() - qs[0].date_uploaded
            ).days

        try:
            context["person_leaflets"] = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            context["person_leaflets"] = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            context["person_leaflets"] = paginator.page(paginator.num_pages)

        return context
