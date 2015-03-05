from django.views.generic import DetailView, ListView
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from leaflets.models import Leaflet
from .forms import ConstituencyLookupForm
from .models import Constituency
from core.helpers import geocode


class ConstituencyView(DetailView):
    model = Constituency

    def get_context_data(self, **kwargs):
        context = super(ConstituencyView, self).get_context_data(**kwargs)
        qs = Leaflet.objects.filter(constituency_id=self.kwargs['pk'])

        paginator = Paginator(qs, 60)
        page = self.request.GET.get('page')
        try:
            context['constituency_leaflets'] = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            context['constituency_leaflets'] = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            context['constituency_leaflets'] = paginator.page(paginator.num_pages)

        return context

class ConstituencyList(ListView):
    form_class = ConstituencyLookupForm
    queryset = Constituency.objects.all()\
               .annotate(num_leaflets=Count('leaflet'))\
               .order_by('-num_leaflets')
    
    def form_valid(self, form):
        location = geocode(form.cleaned_data['postcode'])
        self.success_url = location['constituency'].get_absolute_url()
        return super(HomeView, self).form_valid(form)
