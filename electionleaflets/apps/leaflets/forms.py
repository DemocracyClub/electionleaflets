# coding=utf-8

from collections import OrderedDict
import json
from datetime import timedelta

import requests
from django import forms
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.signing import Signer

from localflavor.gb.forms import GBPostcodeField

from leaflets.models import Leaflet, LeafletImage


class S3UploadedImageField(forms.ImageField):
    def to_python(self, data):
        if not isinstance(data, dict):
            return super().to_python(data)
        content = data.read()
        data.name = content
        if content.startswith("tmp/s3file"):
            return data


class ImagesForm(forms.Form):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "images-image" in self.data:
            self.fields["image"] = forms.CharField(max_length=2000)
        else:
            self.fields["image"] = S3UploadedImageField(
                widget=forms.ClearableFileInput(
                    attrs={"multiple": True, "accept": "image/*",}
                ),
                error_messages={
                    "required": "Please add a photo or skip this step"
                },
            )

    use_required_attribute = False


class PostcodeForm(forms.Form):
    postcode = GBPostcodeField(
        error_messages={
            "required": "Please enter a valid UK postcode",
            "invalid": "Please enter a full UK postcode.",
        }
    )


class LeafletDetailsFrom(forms.ModelForm):
    class Meta:
        model = Leaflet
        fields = "__all__"


class Base64EncodedFileWidget(forms.ClearableFileInput):
    """
    https://github.com/codingjoe/django-s3file/issues/134
    """

    def get_conditions(self, accept):
        conditions = super().get_conditions(accept)
        conditions.append({"Content-Encoding": "base64"})
        return conditions

    input_type = "hidden"
    template_name = "django/forms/widgets/input.html"


class SingleLeafletImageForm(forms.ModelForm):
    class Meta:
        model = LeafletImage
        fields = ["image"]

    image = forms.ImageField(widget=Base64EncodedFileWidget)


class LeafletReviewFrom(forms.ModelForm):
    class Meta:
        model = Leaflet
        fields = ("reviewed",)


class PeopleRadioWidget(forms.RadioSelect):
    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        if not label:
            label = "Not Listed"
        else:
            label = "{0} ({1})".format(
                label["person"]["name"], label["party"]["party_name"],
            )
        return super(PeopleRadioWidget, self).create_option(
            name, value, label, selected, index, subindex, attrs
        )


class PartyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "postcode_results" in kwargs["initial"]:

            postcode_results = kwargs["initial"]["postcode_results"]
            current_parties = set()
            signer = Signer()
            for date in postcode_results["dates"]:
                for ballot in date["ballots"]:
                    # Dead person's switch to ensure this 1:1 mapping of
                    # candidacies to leaflets only happens for #GE2019.
                    # For other ballots, we won't show candidates, just parties.
                    for candidacy in ballot["candidates"]:
                        party_key = signer.sign(
                            json.dumps(
                                {
                                    "party_id": candidacy["party"]["party_id"],
                                    "party_name": candidacy["party"][
                                        "party_name"
                                    ],
                                }
                            )
                        )
                        data = (
                            party_key,
                            candidacy["party"]["party_name"],
                        )
                        current_parties.add(data)
            default_option = [(
                signer.sign(json.dumps({"party_id": None})),
                "Not listed",
            )]
            self.fields["party"] = forms.ChoiceField(
                choices=default_option + list(current_parties),
                widget=forms.RadioSelect,
                required=False,
            )


def clean_party_id(party_id):
    party_map = {
        "joint-party:53-119": ["party:53", "joint-party:53-119"],
        "party:53": ["party:53", "joint-party:53-119"],
    }
    return party_map.get(party_id, [party_id])


class PeopleForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        signer = Signer()
        unsigned_party = json.loads(signer.unsign(kwargs["initial"]["party"]))
        party = clean_party_id(unsigned_party["party_id"])

        if "postcode_results" in kwargs["initial"]:

            postcode_results = kwargs["initial"]["postcode_results"]
            current_parties = set()

            for date in postcode_results["dates"]:
                for ballot in date["ballots"]:
                    for candidacy in ballot["candidates"]:
                        candidacy["ballot"] = {
                            "ballot_paper_id": ballot["ballot_paper_id"],
                            "ballot_title": ballot["ballot_title"]
                        }
                        if candidacy["party"]["party_id"] in party:
                            data = (
                                signer.sign(json.dumps(candidacy)),
                                candidacy["person"]["name"],
                            )
                            current_parties.add(data)
            default_option = [(
                signer.sign(
                json.dumps((None))),
                "Not listed / general party leaflet"

            )]


            self.fields["people"] = forms.MultipleChoiceField(
                choices=default_option + list(current_parties),
                required=False,
                widget=forms.CheckboxSelectMultiple,
            )

class UpdatePublisherDetails(forms.ModelForm):
    class Meta:
        model = Leaflet
        fields = (
            "id",
        )

    def get_ballot_data_from_ynr(self, instance):
        """

        :type instance: Leaflet
        """
        url = f"https://candidates.democracyclub.org.uk/api/next/ballots/"
        params = {"for_postcode": instance.postcode}
        params["election_date_range_after"] = (instance.date_uploaded - timedelta(days=60)).date().isoformat()
        params["election_date_range_before"] = (instance.date_uploaded + timedelta(days=60)).date().isoformat()
        req = requests.get(url, params=params)
        req.raise_for_status()
        return req.json()["results"]

    def get_parties_from_ballot_data(self, ballot_data):
        current_parties = set()
        signer = Signer()
        for ballot in ballot_data:
            for candidacy in ballot["candidacies"]:
                party_key = signer.sign(
                    json.dumps(
                        {
                            "party_id": candidacy["party"]["legacy_slug"],
                            "party_name": candidacy["party"][
                                "name"
                            ],
                        }
                    )
                )
                data = (
                    party_key,
                    candidacy["party"]["name"],
                )
                current_parties.add(data)
        return current_parties

    def get_people_from_ballot_data(self, ballot_data):
        signer = Signer()


        people = set()

        for ballot in ballot_data:
            for candidacy in ballot["candidacies"]:
                candidacy["ballot"] = {
                    "ballot_paper_id": ballot["ballot_paper_id"],
                    "ballot_title": f'{ballot["election"]["name"]}: {ballot["post"]["label"]}'
                }
                data = (
                    signer.sign(json.dumps(candidacy)),
                    candidacy["person"]["name"],
                )
                people.add(data)
        return people



    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.instance and not self.instance.postcode:
            return
        ballot_data= self.get_ballot_data_from_ynr(self.instance)
        self.fields["parties"] = forms.ChoiceField(
            choices=self.get_parties_from_ballot_data(ballot_data),
            widget=forms.RadioSelect,
            required=False,
        )

        self.fields["people"] = forms.MultipleChoiceField(
            choices=self.get_people_from_ballot_data(ballot_data),
            required=False,
            widget=forms.CheckboxSelectMultiple,
        )

    id = forms.CharField(widget=forms.HiddenInput())
