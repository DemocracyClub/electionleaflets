from django.conf.urls import patterns, url

from leaflets.views import (ImageView, LatestLeaflets,
    view_all_full_images, LeafletView, LeafletUploadWizzard,
    skip_inside_allowed, skip_back_allowed, ImageCropView)

from .forms import  (FrontPageImageForm, BackPageImageForm,
    InsidePageImageForm, PostcodeForm)

named_form_list = [
    ('front', FrontPageImageForm),
    ('back', BackPageImageForm),
    ('inside', InsidePageImageForm),
    ('postcode', PostcodeForm),
]

upload_form_wizzard = LeafletUploadWizzard.as_view(named_form_list,
    url_name='upload_step', done_step_name='finished',
    condition_dict={
        'back': skip_back_allowed,
        'inside': skip_inside_allowed,
    }
)

urlpatterns = patterns(
    '',
    url(r'/add/(?P<step>.+)/$', upload_form_wizzard, name='upload_step'),
    url(r'/add/', upload_form_wizzard, name='upload_leaflet'),

    url(r'^/full/(?P<pk>.+)/$',  ImageView.as_view(), name='full_image'),
    url(r'^/crop/(?P<pk>.+)/$',  ImageCropView.as_view(), name='crop'),

    url(r'^/(?P<pk>\d+)/$', LeafletView.as_view(), name='leaflet'),
    url(r'^/$',      LatestLeaflets.as_view(), name='leaflets'),
)

