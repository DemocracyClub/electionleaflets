from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r'leaflets', views.LeafletViewSet)
router.register(r'leafletimages', views.LeafletImageViewSet)
router.register(r'parties', views.PartyViewSet)
router.register(r'constituency', views.ConstituencyViewSet)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls, namespace='api')),
    # url(r'^/$', TemplateView.as_view(
    #     template_name='api/index.html'), name='api_index'),
    url(r'latest.(?P<format>(xml|json))$', views.latest, name='api_latest'),

)
