from django import forms

from localflavor.gb.forms import GBPostcodeField

from .models import Leaflet, LeafletImage
import constants


class ImageForm(forms.Form):
    image = forms.ImageField(widget=forms.FileInput(
        attrs={'accept': "image/*;capture=camera"}))


class FrontPageImageForm(ImageForm):
    pass


class BackPageImageForm(ImageForm):
    pass


class InsidePageImageForm(ImageForm):
    pass


class PostcodeForm(forms.Form):
    postcode = GBPostcodeField()


class LeafletDetailsFrom(forms.ModelForm):
    class Meta:
        model = Leaflet

class LeafletReviewFrom(forms.ModelForm):
    class Meta:
        model = Leaflet
        fields = ('reviewed', )
