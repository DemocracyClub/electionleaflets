from api import views
from django.urls import include, re_path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"leaflets", views.LeafletViewSet)

urlpatterns = [
    re_path(r"^", include((router.urls, "api"))),
]
