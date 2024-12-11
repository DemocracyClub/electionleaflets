from django.urls import path

from .views import PersonView

urlpatterns = [
    path("<int:person_id>/", PersonView.as_view(), name="person"),
]
