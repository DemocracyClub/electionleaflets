import pytest
from django.core.signing import Signer
from django import forms
import json
from analysis.forms import QUESTIONS, QuestionSetForm, CandidateTaggerForm
from analysis.models import LeafletProperties, Leaflet
from django.contrib.auth.models import User



@pytest.mark.django_db
class TestQuestionSetForm:
	@pytest.fixture(autouse=True)
	def setup(self):
		self.leaflet = Leaflet.objects.create()
		self.user = User.objects.create()

	def test_form_initialization(self):
		form = QuestionSetForm(leaflet=self.leaflet, user=self.user)
		assert form.initial["form_name"] == "analysis_questions_1"
		assert "form_name" in form.fields
		assert "leaflet_pk" in form.fields

	def test_form_fields(self):
		form = QuestionSetForm(leaflet=self.leaflet, user=self.user)
		for key in QUESTIONS.keys():
			assert key in form.fields
			assert isinstance(form.fields[key], forms.ChoiceField)

	def test_get_initial_from_models(self):
		LeafletProperties.objects.create(
			leaflet=self.leaflet, key="has_leader", value="Yes", user=self.user
		)
		form = QuestionSetForm(leaflet=self.leaflet, user=self.user)
		form.get_initial_from_models()
		assert form.initial["has_leader"] == "Yes"

	def test_save(self):
		form_data = {
			"form_name": "analysis_questions_1",
			"has_leader": "Yes",
			"leaflet_pk": self.leaflet.pk,
		}
		form = QuestionSetForm(
			leaflet=self.leaflet, user=self.user, data=form_data
		)
		assert form.is_valid()
		form.save()
		assert LeafletProperties.objects.filter(
			leaflet=self.leaflet, key="has_leader", value="Yes"
		).exists()

	def test_save_with_no_answer(self):
		data = {
			"form_name": "analysis_questions_1",
			"has_leader": "",
			"leaflet_pk": self.leaflet.pk,
		}
		form = QuestionSetForm(
			leaflet=self.leaflet, user=self.user, data=data
		)
		assert form.is_valid()
		form.save()
		assert not LeafletProperties.objects.filter(
			leaflet=self.leaflet, key="has_leader"
		).exists()


@pytest.mark.django_db
class TestCandidateTaggerForm:
	@pytest.fixture(autouse=True)
	def setup(self):
		self.user = User.objects.create()
		self.leaflet = Leaflet.objects.create()
		self.instance = LeafletProperties.objects.create(
			leaflet=self.leaflet, user=self.user
		)

		signer = Signer()
		signed_data = signer.sign(
			json.dumps(
				{
					"ynr_party_id": "party:53",
					"ynr_party_name": "Test Party",
					"ballot_id": "ballot123",
					"ynr_person_id": "12345",
					"ynr_person_name": "Test Person",
				}
			)
		)
		form = CandidateTaggerForm(instance=self.instance, data=form_data)
		assert form.is_valid()
		form.save()
		assert form.cleaned_data["people"]["ynr_party_id"] == "party:53"
		assert form.cleaned_data["people"]["ynr_party_name"] == "Test Party"
		assert form.cleaned_data["people"]["ballot_id"] == "ballot123"
		assert form.cleaned_data["people"]["ynr_person_id"] == "12345"
		assert form.cleaned_data["people"]["ynr_person_name"] == "Test Person"
		signer = Signer()
		signed_data = signer.sign("party:53--Test Party")
		form_data = {"parties": signed_data}
		form = CandidateTaggerForm(instance=self.instance, data=form_data)
		assert form.is_valid()
		form.save()
		assert self.instance.ynr_party_id == "party:53"
		assert self.instance.ynr_party_name == "Test Party"
		assert self.instance.ynr_party_name == "Test Party"

