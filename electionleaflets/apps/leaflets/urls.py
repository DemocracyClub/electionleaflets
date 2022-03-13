from django.conf.urls import url
from django.views.decorators.cache import never_cache

from leaflets.views import (
    ImageView,
    LatestLeaflets,
    LeafletView,
    LeafletUploadWizzard,
    ImageCropView,
    AllImageView,
    ImageRotateView,
    LegacyImageView,
    should_show_person_form,
    LeafletUpdatePublisherView,
    should_show_party_form,
    should_show_date_form,
)

from .forms import (
    ImagesForm,
    PostcodeForm,
    PeopleForm,
    PartyForm,
    DateForm,
)

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
    url(
        r"add/(?P<step>.+)/$",
        never_cache(upload_form_wizzard),
        name="upload_step",
    ),
    url(r"add/", never_cache(upload_form_wizzard), name="upload_leaflet"),
    url(r"^full/(?P<pk>\d+)/$", ImageView.as_view(), name="full_image"),
    url(
        r"^full/(?P<pk>.+)/$",
        LegacyImageView.as_view(),
        name="full_image_legacy",
    ),
    url(r"^(?P<pk>\d+)/images/$", AllImageView.as_view(), name="all_images"),
    url(r"^crop/(?P<pk>.+)/$", ImageCropView.as_view(), name="crop"),
    url(r"^rotate/(?P<pk>.+)/$", ImageRotateView.as_view(), name="rotate"),
    url(r"^(?P<pk>\d+)/$", LeafletView.as_view(), name="leaflet"),
    url(
        r"^(?P<pk>\d+)/update_publisher/$",
        LeafletUpdatePublisherView.as_view(),
        name="leaflet_update_publisher_details",
    ),
    url(r"^$", LatestLeaflets.as_view(), name="leaflets"),
]
