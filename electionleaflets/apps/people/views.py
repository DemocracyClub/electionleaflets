from datetime import datetime

from django.views.generic import DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from people.models import Person
from leaflets.models import Leaflet


class PersonView(DetailView):
    model = Person
    template_name = 'people/person.html'
    slug_field = 'remote_id'
    slug_url_kwarg = 'remote_id'

    def get_context_data(self, **kwargs):
        context = super(PersonView, self).get_context_data(**kwargs)
        qs = Leaflet.objects.filter(publisher_person_id=self.object.pk)

        paginator = Paginator(qs, 60)
        page = self.request.GET.get('page')

        if not page or page == 1:
            if qs:
                context['last_leaflet_days'] = \
                    (datetime.now() - qs[0].date_uploaded).days

        try:
            context['person_leaflets'] = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            context['person_leaflets'] = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            context['person_leaflets'] = paginator.page(paginator.num_pages)

        return context
