from analysis.views import TagLeafletList
from django.contrib.auth.decorators import login_required
from django.urls import path

urlpatterns = [
    path(
        r"tag_leaflets/without_party/",
        login_required(TagLeafletList.as_view()),
        name="tag_leaflets_without_party",
    ),
    path(
        r"tag_leaflets/without_people/",
        login_required(TagLeafletList.as_view()),
        name="tag_leaflets",
    ),
]
