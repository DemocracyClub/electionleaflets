from django import forms

from localflavor.gb.forms import GBPostcodeField

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


