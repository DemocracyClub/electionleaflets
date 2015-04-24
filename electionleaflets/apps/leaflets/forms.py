from django import forms

from localflavor.gb.forms import GBPostcodeField

from core.helpers import geocode
from .models import Leaflet, LeafletImage
import constants


class ImageForm(forms.Form):
    image = forms.ImageField(widget=forms.FileInput(
        attrs={'accept': "image/*;capture=camera"}), error_messages={'required': 'Please add a photo or skip this step'})


class FrontPageImageForm(ImageForm):
    pass


class BackPageImageForm(ImageForm):
    pass


class InsidePageImageForm(ImageForm):
    pass


class PostcodeForm(forms.Form):
    postcode = GBPostcodeField(error_messages={'required': 'Please enter a valid UK postcode'})
    wgs84_lon = forms.CharField(
        required=False, max_length=100, widget=forms.HiddenInput())
    wgs84_lat = forms.CharField(
        required=False, max_length=100, widget=forms.HiddenInput())
    constituency = forms.CharField(
        required=False, max_length=255, widget=forms.HiddenInput())

    def clean_postcode(self):
        postcode = self.cleaned_data['postcode']
        self.geo_data = geocode(postcode)
        if not self.geo_data or 'constituency' not in self.geo_data:
            raise forms.ValidationError("Please enter a full valid UK postcode")
        return postcode

    def clean(self):
        data = super(PostcodeForm, self).clean()
        if hasattr(self, 'geo_data') and self.geo_data:
            data['constituency'] = self.geo_data['constituency']
            data['wgs84_lon'] = self.geo_data['wgs84_lon']
            data['wgs84_lat'] = self.geo_data['wgs84_lat']
        else:
            raise forms.ValidationError("Please enter a full valid UK postcode")
        return data

class LeafletDetailsFrom(forms.ModelForm):
    class Meta:
        model = Leaflet

class LeafletReviewFrom(forms.ModelForm):
    class Meta:
        model = Leaflet
        fields = ('reviewed', )

class PeopleModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class PeopleForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PeopleForm, self).__init__(*args, **kwargs)
        self.fields['people'] = \
            PeopleModelChoiceField(
                queryset=kwargs['initial']['_people'],
                widget=forms.RadioSelect,
                empty_label="Not listed",
                required=False)


