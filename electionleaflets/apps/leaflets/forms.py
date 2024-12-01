# coding=utf-8
import json
from datetime import timedelta
from urllib.parse import urljoin

import requests
from django import forms
from django.conf import settings
from django.core.signing import Signer
from django.utils import timezone
from leaflets.fields import DCDateField
from leaflets.models import Leaflet, LeafletImage
from localflavor.gb.forms import GBPostcodeField


class S3UploadedImageField(forms.ImageField):
    def to_python(self, data):
        if not isinstance(data, dict):
            return super().to_python(data)
        content = data.read()
        data.name = content
        if content.startswith("tmp/s3file"):
            return data
        return None


class ImagesForm(forms.Form):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "images-image" in self.data:
            self.fields["image"] = forms.CharField(max_length=2000)
        else:
            self.fields["image"] = S3UploadedImageField(
                widget=forms.ClearableFileInput(
                    attrs={
                        "accept": "image/*",
                    }
                ),
                error_messages={
                    "required": "Please add a photo or skip this step"
                },
            )

    use_required_attribute = False


class PostcodeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # assign a (computed, I assume) default value to the choice field
        self.initial["delivered"] = "now"

    postcode = GBPostcodeField(
        error_messages={
            "required": "Please enter a valid UK postcode",
            "invalid": "Please enter a full UK postcode.",
        }
    )

    delivered = forms.ChoiceField(
        choices=(
            ("now", "In the last couple of weeks"),
            ("before", "Some time ago"),
        ),
        widget=forms.RadioSelect,
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
                label["person"]["name"],
                label["party"]["party_name"],
            )
        return super(PeopleRadioWidget, self).create_option(
            name, value, label, selected, index, subindex, attrs
        )


class YNRBallotDataMixin:
    FOR_DATE = None

    def get_date_range(self):
        for_date = self.FOR_DATE
        if not for_date:
            for_date = timezone.now()
        print(for_date, self.FOR_DATE)
        start = (for_date - timedelta(days=60)).date().isoformat()
        end = (for_date + timedelta(days=60)).date().isoformat()
        return (start, end)

    def get_ballot_data_from_ynr(self, postcode):
        """

        :type instance: Leaflet
        """
        url = urljoin(settings.YNR_BASE_URL, "/api/next/ballots/")
        auth_token = getattr(settings, "YNR_API_KEY")
        params = {"for_postcode": postcode, "auth_token": auth_token}
        start, end = self.get_date_range()
        params["election_date_range_after"] = start
        params["election_date_range_before"] = end
        try:
            req = requests.get(url, params=params)
        except requests.RequestException:
            return []
        req.raise_for_status()
        return req.json()["results"]

    def get_parties_from_ballot_data(self, ballot_data):
        parties = {
            "party:52": "Conservative and Unionist Party",
            "party:63": "Green Party",
            "ynmp-party:2": "Independent",
            "party:53": "Labour Party",
            "party:90": "Liberal Democrats",
            "party:77": "Plaid Cymru - The Party of Wales",
            "party:102": "Scottish National Party (SNP)",
        }

        current_parties = set()
        signer = Signer()
        parties_with_candidates = set()
        for ballot in ballot_data:
            for candidacy in ballot["candidacies"]:
                parties_with_candidates.add(candidacy["party"]["legacy_slug"])
                parties[candidacy["party"]["legacy_slug"]] = candidacy["party"][
                    "name"
                ]

        for party_id, party_name in parties.items():
            party_key = signer.sign(
                json.dumps(
                    {
                        "party_id": party_id,
                        "party_name": party_name,
                        "has_candidates": party_id in parties_with_candidates,
                    }
                )
            )
            data = (
                party_key,
                party_name,
            )
            current_parties.add(data)
        return current_parties

    def get_people_from_ballot_data(self, ballot_data, party=None):
        signer = Signer()

        people = set()

        for ballot in ballot_data:
            for candidacy in ballot["candidacies"]:
                if party and candidacy["party"]["legacy_slug"] not in party:
                    continue
                candidacy["ballot"] = {
                    "ballot_paper_id": ballot["ballot_paper_id"],
                    "ballot_title": f'{ballot["election"]["name"]}: {ballot["post"]["label"]}',
                }
                data = (
                    signer.sign(json.dumps(candidacy)),
                    candidacy["person"]["name"],
                )
                people.add(data)
        return people


class PartyForm(YNRBallotDataMixin, forms.Form):
    party = forms.ChoiceField(
        choices=[],
        widget=forms.RadioSelect,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "postcode" not in self.initial:
            return

        self.FOR_DATE = kwargs.get("initial", {}).pop("for_date", None)
        ballot_data = self.get_ballot_data_from_ynr(self.initial["postcode"])
        self.fields["party"] = forms.ChoiceField(
            choices=list(self.get_parties_from_ballot_data(ballot_data))
            + [(None, "Party not listed")],
            widget=forms.RadioSelect,
            required=False,
        )


def clean_party_id(party_id):
    party_map = {
        "joint-party:53-119": ["party:53", "joint-party:53-119"],
        "party:53": ["party:53", "joint-party:53-119"],
    }
    return party_map.get(party_id, [party_id])


class PeopleForm(YNRBallotDataMixin, forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.FOR_DATE = kwargs.get("initial", {}).pop("for_date", None)
        signer = Signer()
        unsigned_party = json.loads(signer.unsign(kwargs["initial"]["party"]))
        party = clean_party_id(unsigned_party["party_id"])
        ballot_data = self.get_ballot_data_from_ynr(self.initial["postcode"])

        self.fields["people"] = forms.MultipleChoiceField(
            choices=self.get_people_from_ballot_data(ballot_data, party=party),
            required=False,
            widget=forms.CheckboxSelectMultiple,
        )


class DateForm(forms.Form):
    date = DCDateField(required=False)


class UpdatePublisherDetails(YNRBallotDataMixin, forms.ModelForm):
    class Meta:
        model = Leaflet
        fields = ("id",)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.instance and not self.instance.postcode:
            return
        ballot_data = self.get_ballot_data_from_ynr(self.instance.postcode)
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

    def get_date_range(self):
        start = (
            (self.instance.date_uploaded - timedelta(days=60))
            .date()
            .isoformat()
        )
        end = (
            (self.instance.date_uploaded + timedelta(days=60))
            .date()
            .isoformat()
        )
        return (start, end)
