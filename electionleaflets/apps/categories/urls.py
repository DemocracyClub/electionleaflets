from django.conf.urls import patterns, include, handler500, url
from django.conf import settings

from django.views.generic import TemplateView

from categories.views import view_category

urlpatterns = [
    url(r'^$', TemplateView.as_view(
        template_name='categories/index.html'
    ), name='categories'),
    url(r'^(?P<slug>[\w_\-\.]+)/$',  view_category, name='category'),
]
