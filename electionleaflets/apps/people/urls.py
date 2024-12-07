from django.urls import re_path

from .views import PersonView

urlpatterns = [
    re_path(r"^(?P<person_id>\d+)/$", PersonView.as_view(), name="person"),
]
