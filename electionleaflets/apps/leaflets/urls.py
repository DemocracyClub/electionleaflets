from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from django.views.decorators.cache import never_cache
from leaflets.views import (
    ElectionIDView,
    ImageCropView,
    ImageRotateView,
    ImageView,
    LatestLeaflets,
    LeafletModeration,
    LeafletUpdatePublisherView,
    LeafletUploadWizzard,
    LeafletView,
    LegacyImageView,
    should_show_date_form,
    should_show_person_form,
)

from .forms import DateForm, ImagesForm, PartyForm, PeopleForm, PostcodeForm

named_form_list = [
    ("images", ImagesForm),
    ("postcode", PostcodeForm),
    ("date", DateForm),
    ("party", PartyForm),
    ("people", PeopleForm),
]

upload_form_wizzard = LeafletUploadWizzard.as_view(
    named_form_list,
    url_name="upload_step",
    done_step_name="finished",
    condition_dict={
        "people": should_show_person_form,
        "date": should_show_date_form,
    },
)

urlpatterns = [
    re_path(
        r"add/(?P<step>.+)/$",
        never_cache(upload_form_wizzard),
        name="upload_step",
    ),
    re_path(r"add/", never_cache(upload_form_wizzard), name="upload_leaflet"),
    re_path(r"^full/(?P<pk>\d+)/$", ImageView.as_view(), name="full_image"),
    re_path(
        r"^full/(?P<pk>.+)/$",
        LegacyImageView.as_view(),
        name="full_image_legacy",
    ),
    re_path(r"^crop/(?P<pk>.+)/$", ImageCropView.as_view(), name="crop"),
    re_path(r"^rotate/(?P<pk>.+)/$", ImageRotateView.as_view(), name="rotate"),
    re_path(r"^(?P<pk>\d+)/$", LeafletView.as_view(), name="leaflet"),
    re_path(
        r"^(?P<pk>\d+)/update_publisher/$",
        LeafletUpdatePublisherView.as_view(),
        name="leaflet_update_publisher_details",
    ),
    re_path(r"^$", LatestLeaflets.as_view(), name="leaflets"),
    path(
        r"election/<str:election_id>/",
        ElectionIDView.as_view(),
        name="leaflet_by_election_id",
    ),
    re_path(
        r"^moderate$",
        login_required(LeafletModeration.as_view()),
        name="moderate",
    ),
]
