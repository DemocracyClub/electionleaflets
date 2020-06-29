from django.conf.urls import include, url

from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r'leaflets', views.LeafletViewSet)
router.register(r'leafletimages', views.LeafletImageViewSet)
router.register(r'parties', views.PartyViewSet)
router.register(r'constituency', views.ConstituencyViewSet)
router.register(r'ballots', views.LeafletsByBallotView, basename="ballot")

urlpatterns = [
    url(r'^', include((router.urls, 'api'))),
    url(r'stats', views.StatsView.as_view()),
    url(r'latest_by_constituency', views.LatestByConstituencyView.as_view()),
    url(r'latest_by_person', views.LatestByPersonView.as_view()),
]
