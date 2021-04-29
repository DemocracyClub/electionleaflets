# coding=utf-8

from collections import OrderedDict
import json

from django import forms
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.signing import Signer

from localflavor.gb.forms import GBPostcodeField

from leaflets.models import Leaflet, LeafletImage

class S3UploadedImageField(forms.ImageField):
    def to_python(self, data):
        if not isinstance(data, ContentFile):
            return super().to_python(data)
        content =data.read()
        data.name = content
        if content.startswith("tmp/s3file"):
            return data

class ImagesForm(forms.Form):
    use_required_attribute = False
    image = S3UploadedImageField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        error_messages={"required": "Please add a photo or skip this step"},
    )


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


class PeopleForm(forms.Form):
    # A temporary top-X list of parties per register to show if the candidate
    # isn't shown. We will eventually create this list based on real data.
    HARDCODED_PARTIES = {
        "gb": [
            (52, "Conservative and Unionist Party"),
            (63, "Green Party"),
            (53, "Labour Party"),
            (90, "Liberal Democrats"),
            (102, "Scottish National Party (SNP)"),
            (7931, "Reform UK"),
            (77, "Plaid Cymru - The Party of Wales"),
        ],
        "ni": [
            (103, "Alliance - Alliance Party of Northern Ireland"),
            (70, "Democratic Unionist Party - D.U.P."),
            (55, "SDLP (Social Democratic & Labour Party)"),
            (39, "Sinn Féin"),
            (83, "Ulster Unionist Party"),
        ],
    }

    def __init__(self, *args, **kwargs):
        super(PeopleForm, self).__init__(*args, **kwargs)
        signer = Signer()

        if "postcode_results" in kwargs["initial"]:

            postcode_results = kwargs["initial"]["postcode_results"].json()

            # We have a response, parse each candidacy in to a set
            # of unique people as people can stand in more than one ballot
            # for a postcode
            unique_people = OrderedDict()
            for date in postcode_results["dates"]:
                for ballot in date["ballots"]:
                    # Dead person's switch to ensure this 1:1 mapping of
                    # candidacies to leaflets only happens for #GE2019.
                    # For other ballots, we won't show candidates, just parties.
                    if ballot["ballot_paper_id"].startswith("parl.") and ballot[
                        "ballot_paper_id"
                    ].endswith(".2019-12-12"):
                        for candidacy in ballot["candidates"]:
                            # Until we have better live lookup of YNR in EL, we'll
                            # embed the results in our form fields. Not ideal. We'll
                            # sign the data so people can't inject garbage into the
                            # database.
                            data = {
                                "ynr_party_id": candidacy["party"]["party_id"],
                                "ynr_party_name": candidacy["party"][
                                    "party_name"
                                ],
                                "ynr_person_id": candidacy["person"]["ynr_id"],
                                "ynr_person_name": candidacy["person"]["name"],
                                "ballot_id": ballot["ballot_paper_id"],
                            }
                            person_key = signer.sign(json.dumps(data))
                            unique_people[person_key] = candidacy

            self.fields["people"] = forms.ChoiceField(
                choices=list(unique_people.items()),
                widget=PeopleRadioWidget,
                required=False,
            )
            if (
                "electoral_services" in postcode_results
                and postcode_results["electoral_services"]["council_id"][0:3]
                == "N09"
            ):
                parties = self.HARDCODED_PARTIES["ni"]
            else:
                parties = self.HARDCODED_PARTIES["gb"]

        else:
            parties = (
                self.HARDCODED_PARTIES["gb"] + self.HARDCODED_PARTIES["ni"]
            )

        party_options = []
        for party in parties:
            party_options.append(
                (
                    signer.sign("party:{0}--{1}".format(party[0], party[1])),
                    party[1],
                )
            )

        party_options.append((signer.sign("--"), "Not Listed"))

        self.fields["parties"] = forms.ChoiceField(
            choices=party_options, widget=forms.RadioSelect, required=False
        )
