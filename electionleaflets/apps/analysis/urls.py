from django.conf.urls import patterns, include, handler500, url
from django.conf import settings

from django.views.generic import TemplateView

urlpatterns = patterns(
    '',
    url(r'^/$', TemplateView.as_view(template_name='analysis/index.html'),
        name='analysis'),
    url(r'^/new$', TemplateView.as_view(template_name='analysis/index1.html'),
        name='analysis_new'),
    url(r'^/task$', TemplateView.as_view(template_name='analysis/task.html'),
    name='task'),
)

