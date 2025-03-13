from analysis.views import (
    WithoutPartyTagLeafletList,
    WithoutPeopleTagLeafletList,
)
from django.contrib.auth.decorators import login_required
from django.urls import path

urlpatterns = [
    path(
        r"tag_leaflets/without_party/",
        login_required(WithoutPartyTagLeafletList.as_view()),
        name="tag_leaflets_without_party",
    ),
    path(
        r"tag_leaflets/without_people/",
        login_required(WithoutPeopleTagLeafletList.as_view()),
        name="tag_leaflets",
    ),
]
