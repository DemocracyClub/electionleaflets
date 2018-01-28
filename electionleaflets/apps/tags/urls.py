from django.conf.urls import url

from django.views.generic import TemplateView

from tags.views import view_tag, TagList

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='tags/index.html'), name='tags'),
    url(r'^(?P<pk>\d+)/$', TagList.as_view(), name='tag'),
    url(r'^(?P<slug>[\w_\-\.]+)/$', view_tag, name='tag'),
]
