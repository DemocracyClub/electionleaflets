from django.http import Http404
from django.views.generic import ListView
from leaflets.models import Leaflet


class PersonView(ListView):
    template_name = "people/person.html"
    paginate_by = 50

    def get_queryset(self):
        return Leaflet.objects.filter(
            person_ids__contains=self.kwargs["person_id"]
        )

    def get_context_data(self, **kwargs):
        context = super(PersonView, self).get_context_data(**kwargs)
        if not context["object_list"].exists():
            raise Http404(
                f"No leaflets found for person {self.kwargs['person_id']}"
            )
        person_id = str(self.kwargs["person_id"])
        leaflet_people = context["object_list"].first().people
        context["person"] = leaflet_people.get(person_id)["person"]

        return context
