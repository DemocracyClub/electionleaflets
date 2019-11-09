from collections import OrderedDict

from django import forms

from localflavor.gb.forms import GBPostcodeField

from core.helpers import geocode
from leaflets.models import Leaflet


class ImageForm(forms.Form):
    use_required_attribute = False
    image = forms.ImageField(widget=forms.FileInput(
        attrs={'accept': "image/*;capture=camera"}),
        error_messages={'required': 'Please add a photo or skip this step'})


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
        fields = '__all__'


class LeafletReviewFrom(forms.ModelForm):
    class Meta:
        model = Leaflet
        fields = ('reviewed', )


class PeopleRadioWidget(forms.RadioSelect):

    def create_option(self, name, value, label, selected, index, subindex=None,
                      attrs=None):
        if not label:
            label = "Not Listed"
        else:
            label = "{0} ({1})".format(
                label["person"]["name"],
                label["party"]["party_name"],
            )
        return super(PeopleRadioWidget, self).create_option(name, value, label, selected, index,
                                     subindex, attrs)


class PeopleForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PeopleForm, self).__init__(*args, **kwargs)
        if "postcode_results" in kwargs['initial']:
            postcode_results = kwargs['initial']["postcode_results"]

            # We have a response, parse each candidacy in to a set
            # of unique people as people can stand in more than one ballot
            # for a postcode
            unique_people = OrderedDict()
            for date in postcode_results.json()["dates"]:
                for ballot in date["ballots"]:
                    for candidacy in ballot["candidates"]:
                        person_key = "--".join([
                            str(candidacy['person']['ynr_id']),
                            candidacy["party"]["party_id"]
                        ])
                        unique_people[person_key] = candidacy

            unique_people['not_listed'] = None
            self.fields['people'] = \
                forms.ChoiceField(
                    choices=unique_people.items(),
                    widget=PeopleRadioWidget,
                    required=False)
