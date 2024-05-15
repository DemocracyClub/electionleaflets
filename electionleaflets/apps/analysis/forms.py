import json
from collections import OrderedDict

from django import forms
from django.core.signing import Signer
from leaflets.forms import PeopleForm
from people.models import Person

from .models import LeafletProperties

QUESTIONS = OrderedDict(
    [
        (
            "has_leader",
            {
                "label": "Party leader mentioned",
                "help_text": "Is the party leader mentioned?",
                "choices": ("Yes", "No", "n/a"),
            },
        ),
        (
            "has_leader_photo",
            {
                "label": "Leader photo",
                "help_text": "Is there a photo of the sending party's leader?",
                "choices": ("Yes", "No", "n/a"),
            },
        ),
        (
            "leaflet_style",
            {
                "label": "Leaflet Style",
                "choices": (
                    "Leaflet",
                    "Letter",
                    "Magazine",
                    "Newsletter",
                    "Newspaper",
                    "CV",
                    "Survey",
                ),
            },
        ),
        (
            "has_opposition_leader",
            {
                "label": "Opposition leader pictured",
                "help_text": "Is there a photo of the another party leader?",
                "choices": ("Yes", "No", "n/a"),
            },
        ),
        (
            "has_opposition_leader_photo",
            {
                "label": "Opposition leader mentioned",
                "help_text": "Is another party leader mentioned?",
                "choices": ("Yes", "No", "n/a"),
            },
        ),
        (
            "has_logo",
            {
                "label": "Party logo",
                "help_text": "Is the sending party's logo on this leaflet?",
                "choices": ("Yes", "No", "n/a"),
            },
        ),
        (
            "squeeze_message",
            {
                "label": "Is there a 'squeeze message'?",
                "help_text": "i.e. does it say 'only X party can win here', 'X party can't win here', 'its a two-horse race', or a variation on that",
                "choices": ("Yes", "No", "n/a"),
            },
        ),
        (
            "include_graph",
            {
                "label": "Does it include a graph?",
                "choices": ("Yes", "No", "n/a"),
            },
        ),
    ]
)


class QuestionSetForm(forms.ModelForm):
    class Meta:
        model = LeafletProperties
        fields = "__all__"

    def __init__(self, leaflet, user, *args, **kwargs):
        super(QuestionSetForm, self).__init__(*args, **kwargs)
        self.leaflet = leaflet
        self.user = user
        self.fields = OrderedDict(
            {
                "form_name": forms.CharField(widget=forms.HiddenInput),
                "leaflet_pk": forms.CharField(
                    widget=forms.HiddenInput, required=False,
                ),
            }
        )

        self.initial["form_name"] = "analysis_questions_1"
        self.get_initial_from_models()

        for key, value in list(QUESTIONS.items()):
            self.fields[key] = forms.ChoiceField(
                label=value["label"],
                choices=[(v, v) for v in value["choices"]],
                widget=forms.RadioSelect,
                help_text=value.get("help_text", None),
                required=False,
            )

    def get_initial_from_models(self):
        for question in LeafletProperties.objects.filter(leaflet=self.leaflet):
            self.initial[question.key] = question.value

    def save(self, *args, **kwargs):
        for question, answer in list(self.cleaned_data.items()):
            if not answer:
                continue
            if question in list(QUESTIONS.keys()):
                question, created = LeafletProperties.objects.update_or_create(
                    leaflet=self.leaflet,
                    user=self.user,
                    key=question,
                    defaults={"value": answer},
                )


class CandidateTaggerForm(PeopleForm):
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance")
        super(CandidateTaggerForm, self).__init__(*args, **kwargs)

    def save(self):

        if "people" in self.cleaned_data and self.cleaned_data["people"]:
            signer = Signer()
            data = json.loads(signer.unsign(self.cleaned_data["people"]))
            self.instance.ynr_party_id = data["ynr_party_id"]
            self.instance.ynr_party_name = data["ynr_party_name"]
            self.instance.ballot_id = data["ballot_id"]
            person, _ = Person.objects.get_or_create(
                remote_id=data["ynr_person_id"],
                defaults={
                    "name": data["ynr_person_name"],
                    "source_url": "https://candidates.democracyclub.org.uk/person/{}".format(
                        data["ynr_person_id"]
                    ),
                    "source_name": "YNR2017",
                },
            )
            self.instance.publisher_person = person

        elif self.cleaned_data.get("parties") and self.cleaned_data["parties"]:
            signer = Signer()
            (
                self.instance.ynr_party_id,
                self.instance.ynr_party_name,
            ) = signer.unsign(self.cleaned_data["parties"]).split("--")

        self.instance.save()
