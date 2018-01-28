from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404


def view_category(request, slug):
    from categories.models import Category
    from leaflets.models import Leaflet
    import math

    category = get_object_or_404(Category, slug=slug)

    qs = Leaflet.objects.filter(categories__id=category.id).order_by('-id')
    total = qs.count()
    currentPage = request.GET.get('page', 1)
    totalPages = int(math.ceil(float(total) / 12))

    return render_to_response('categories/category.html',
                              {
                                  'category': category,
                                  'qs': qs,
                                  'total': total,
                                  'currentPage': currentPage,
                                  'totalPages': totalPages,
                                  'request': request
                              },
                              context_instance=RequestContext(request))
