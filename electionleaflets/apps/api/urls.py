from api import views
from django.conf.urls import include, url
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"leaflets", views.LeafletViewSet)

urlpatterns = [
    url(r"^", include((router.urls, "api"))),
]
