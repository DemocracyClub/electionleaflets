import json
import datetime
import random

from django.db import transaction
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib import messages
from django.urls import reverse
from formtools.wizard.views import NamedUrlSessionWizardView
from django.core.signing import Signer
from django.conf import settings
from django.views.generic import DetailView, ListView, UpdateView, RedirectView
from django.views.generic.detail import SingleObjectMixin
from braces.views import StaffuserRequiredMixin, LoginRequiredMixin

from analysis.forms import QuestionSetForm
from core.helpers import CacheControlMixin
from .models import Leaflet, LeafletImage
from .forms import (
    LeafletDetailsFrom,
    SingleLeafletImageForm,
    UpdatePublisherDetails,
)
from people.models import Person
from storages.backends.s3boto3 import S3Boto3Storage


class ImageView(CacheControlMixin, UpdateView):
    cache_timeout = 60 * 60
    model = LeafletImage
    template_name = "leaflets/full.html"
    form_class = SingleLeafletImageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["full_width"] = True
        # context["image_form"] = SingleLeafletImageForm(instance=self.object)
        return context


class LegacyImageView(SingleObjectMixin, RedirectView):
    model = LeafletImage
    permanent = True

    def get_object(self, queryset=None):
        key = self.kwargs.get(self.pk_url_kwarg, None)
        return LeafletImage.objects.filter(legacy_image_key=key)[0]

    def get_redirect_url(self, *args, **kwargs):
        return self.get_object().get_absolute_url()


class AllImageView(UpdateView):
    model = Leaflet
    form_class = LeafletDetailsFrom
    template_name = "leaflets/full_all.html"


class ImageRotateView(StaffuserRequiredMixin, DetailView):
    model = LeafletImage
    template_name = "leaflets/image_rotate.html"

    def post(self, request, *args, **kwargs):
        image_model = self.get_object()
        rotation = request.POST.get("rotate")
        print(rotation)
        image_model.rotate(int(rotation))
        return HttpResponseRedirect(image_model.get_absolute_url())


class ImageCropView(StaffuserRequiredMixin, DetailView):
    model = LeafletImage
    template_name = "leaflets/image_crop.html"

    def post(self, request, *args, **kwargs):
        image_model = self.get_object()
        x = int(request.POST.get("x"))
        y = int(request.POST.get("y"))
        x2 = int(request.POST.get("x2"))
        y2 = int(request.POST.get("y2"))

        image_model.crop(x, y, x2, y2)
        return HttpResponseRedirect(image_model.get_absolute_url())


class LatestLeaflets(CacheControlMixin, ListView):
    cache_timeout = 60 * 60
    model = Leaflet
    template_name = "leaflets/index.html"
    paginate_by = 60


class LeafletView(CacheControlMixin, DetailView):
    cache_timeout = 60 * 60
    template_name = "leaflets/leaflet.html"
    model = Leaflet

    def get_context_data(self, **kwargs):
        context = super(LeafletView, self).get_context_data(**kwargs)
        context["analysis_form"] = QuestionSetForm(
            self.object, self.request.user
        )

        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()

        self.object = self.get_object()
        form = QuestionSetForm(self.object, self.request.user, request.POST,)

        if form.is_valid():
            form.save()
            if "save_and_next" in request.POST:
                start_date = datetime.date(2015, 1, 1)
                next_leaflet = (
                    Leaflet.objects.filter(leafletproperties=None)
                    .filter(date_uploaded__gt=start_date)
                    .order_by("?")
                )
                if next_leaflet:
                    url = next_leaflet[0].get_absolute_url()
                    return HttpResponseRedirect(url)
            return HttpResponseRedirect(self.object.get_absolute_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


def should_show_party_form(wizard):
    party_form = wizard.get_form("party")
    postcode_dict = wizard.get_cleaned_data_for_step("postcode")

    if not postcode_dict:
        return False
    postcode = postcode_dict.get("postcode")
    ballot_data = party_form.get_ballot_data_from_ynr(postcode)
    if not ballot_data:
        return False
    return True


def should_show_person_form(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step("party") or {}
    if not cleaned_data:
        return False
    if cleaned_data.get("party"):
        signer = Signer()
        selected_party = json.loads(signer.unsign(cleaned_data["party"]))
        return selected_party.get("has_candidates", False)


def should_show_date_form(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step("postcode") or {}
    if not cleaned_data:
        return False
    if cleaned_data.get("delivered") == "before":
        return True


class LeafletUploadWizzard(NamedUrlSessionWizardView):
    extra_added = False
    file_storage = S3Boto3Storage()

    storage_name = "core.storage_helpers.PreUploadedSessionStorage"

    TEMPLATES = {
        "images": "leaflets/upload_form/images.html",
        "postcode": "leaflets/upload_form/postcode.html",
        "date": "leaflets/upload_form/date.html",
        "party": "leaflets/upload_form/party.html",
        "people": "leaflets/upload_form/people.html",
    }

    def get_template_names(self):
        step_name = self.steps.current
        return [self.TEMPLATES[step_name]]

    def get_form_initial(self, step):
        if step in ["party", "people"]:
            postcode = self.get_cleaned_data_for_step("postcode")
            if not postcode:
                return
            ret = {"postcode": postcode.get("postcode")}
            if self.get_cleaned_data_for_step("date"):
                ret["for_date"] = self.get_cleaned_data_for_step("date")["date"]

            party_data = self.storage.get_step_data("party")
            if not party_data:
                return ret

            if step == "people":
                ret["party"] = self.storage.get_step_data("party")[
                    "party-party"
                ]
            return ret

    def get_context_data(self, **kwargs):
        context = super(LeafletUploadWizzard, self).get_context_data(**kwargs)
        context["hide_footer"] = True
        return context

    def get(self, *args, **kwargs):
        if "reset" in self.request.GET:
            self.storage.reset()
            return HttpResponseRedirect("/")
        return super(LeafletUploadWizzard, self).get(*args, **kwargs)

    
    def copy_file(self, bucket, file_path, new_file_name):
        copy_source = {
            "Bucket": bucket.name,
            "Key": file_path,
        }
        moved_file = bucket.Object(new_file_name)
        moved_file.copy(copy_source)
        return moved_file
                    
    @transaction.atomic
    def done(self, form_list, **kwargs):
        # Create a new leaflet
        leaflet = Leaflet()
        leaflet.save()
        signer = Signer()
        for form in form_list:
            form_prefix = form.prefix.split("-")[0]

            if form_prefix == "images":
                # Dealing with an image form
                images_text = self.storage.get_step_data("images")[
                    "images-image"
                ]
                try:
                    uploaded_images = json.loads(images_text)
                except json.JSONDecodeError:
                    messages.error(
                        self.request,
                        "There was an error processing the leaflet images. Please ensure Javascript is enabled and try again.",
                    )
                    leaflet.delete()
                    return redirect(reverse("upload_leaflet"))
                
                uploaded_images = json.loads(images_text)

                for file_path in uploaded_images:
                    file_name = file_path.split("/")[-1]
                    file_name = file_name.replace(" ", "-")
                    
                    storage_backend = getattr(settings, 'DEFAULT_FILE_STORAGE')

                    new_file_name = f"leaflets/{leaflet.pk}/{file_name}"

                    if storage_backend == "storages.backends.s3boto3.S3Boto3Storage":
                        bucket = self.storage.file_storage.bucket
                        moved_file = self.copy_file(bucket, file_path, new_file_name)
                        new_file_name_raw = f"raw_{new_file_name}"
                        moved_file_raw = self.copy_file(bucket, file_path, new_file_name_raw) 
                    else:
                        new_file_name_raw = f"raw_{new_file_name}"
                        
                    image = LeafletImage(leaflet=leaflet)
                    image.image.name = new_file_name
                    image.raw_image.name = new_file_name_raw
                    image.save()

            if form_prefix == "postcode":
                leaflet.postcode = form.cleaned_data["postcode"]

            if form_prefix == "party" and form.cleaned_data["party"]:
                party_data = json.loads(
                    signer.unsign(form.cleaned_data["party"])
                )
                if party_data["party_id"]:
                    leaflet.ynr_party_id = party_data["party_id"]
                    leaflet.ynr_party_name = party_data["party_name"]

            if form_prefix == "people":
                if (
                    "people" in form.cleaned_data
                    and isinstance(form.cleaned_data["people"], list)
                    and form.cleaned_data["people"] != ""
                ):
                    leaflet_people = {}
                    for person in form.cleaned_data["people"]:

                        person_data = json.loads(signer.unsign(person))
                        if not person_data:
                            continue
                        leaflet_people[
                            person_data["person"]["id"]
                        ] = person_data
                        person, _ = Person.objects.get_or_create(
                            remote_id=person_data["person"]["id"],
                            defaults={
                                "name": person_data["person"]["name"],
                                "source_url": "https://candidates.democracyclub.org.uk/person/{}".format(
                                    person_data["person"]["id"]
                                ),
                                "source_name": "YNR2017",
                            },
                        )

                    leaflet.people = leaflet_people
                    leaflet.person_ids = list(leaflet_people.keys())
                    leaflet.ballots = [
                        c["ballot"] for ynr_id, c in leaflet_people.items()
                    ]

        leaflet.save()
        messages.success(
            self.request, random.sample(settings.THANKYOU_MESSAGES, 1)[0]
        )
        self.storage.reset()
        return redirect(reverse("leaflet", kwargs={"pk": leaflet.pk}))


class LeafletUpdatePublisherView(LoginRequiredMixin, UpdateView):
    model = Leaflet
    form_class = UpdatePublisherDetails
    template_name = "leaflets/leaflet_update_publisher.html"

    def get_success_url(self):
        return self.object.get_absolute_url()

    @transaction.atomic
    def form_valid(self, form):
        signer = Signer()
        leaflet_people = {}
        for person in form.cleaned_data["people"]:

            person_data = json.loads(signer.unsign(person))
            if not person_data:
                continue
            leaflet_people[person_data["person"]["id"]] = person_data
            person, _ = Person.objects.get_or_create(
                remote_id=person_data["person"]["id"],
                defaults={
                    "name": person_data["person"]["name"],
                    "source_url": "https://candidates.democracyclub.org.uk/person/{}".format(
                        person_data["person"]["id"]
                    ),
                    "source_name": "YNR2017",
                },
            )

        self.object.people = leaflet_people
        self.object.person_ids = list(leaflet_people.keys())
        self.object.ballots = [
            c["ballot"] for ynr_id, c in leaflet_people.items()
        ]

        party_data = json.loads(signer.unsign(form.cleaned_data["parties"]))
        if party_data["party_id"]:
            self.object.ynr_party_id = party_data["party_id"]
            self.object.ynr_party_name = party_data["party_name"]

        return super().form_valid(form)


class LeafletModeration(ListView):
    queryset = Leaflet.objects.filter(status="draft")[:10]
    template_name = "leaflets/moderation_queue.html"


    def post(self, request):
        leaflet = Leaflet.objects.get(pk=self.request.POST.get("leaflet"))
        leaflet.status = "live"
        leaflet.save()
        return HttpResponseRedirect(reverse("moderate"))