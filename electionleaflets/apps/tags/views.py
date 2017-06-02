from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import ListView

from tags.models import Tag


def view_tag(request, slug):
    from tags.models import Tag
    from leaflets.models import Leaflet
    from categories.models import Category
    import math

    tag = get_object_or_404(Tag, slug=slug)

    qs = Leaflet.objects.filter(tags__id=tag.id).order_by('-id')
    total = qs.count()

    currentPage = request.GET.get('page', 1)
    totalPages = int(math.ceil(float(total) / 12))

    return render_to_response('tags/tag.html',
                              {
                                  'tag': tag,
                                  'qs': qs,
                                  'total': total,
                                  'currentPage': currentPage,
                                  'totalPages': totalPages,
                                  'request': request,
                              },
                              context_instance=RequestContext(request))


class TagList(ListView):
    template_name = 'tags/index.html'
    queryset = Tag.objects.all()
