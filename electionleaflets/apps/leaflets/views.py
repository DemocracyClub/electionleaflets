import json
import datetime
import random

from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib import messages
from django.urls import reverse
from formtools.wizard.views import NamedUrlSessionWizardView
from django.core.signing import Signer
from django.conf import settings
from django.views.generic import DetailView, ListView, UpdateView, RedirectView
from django.views.generic.detail import SingleObjectMixin
from braces.views import StaffuserRequiredMixin

from analysis.forms import QuestionSetForm
from .models import Leaflet, LeafletImage
from .forms import LeafletDetailsFrom, SingleLeafletImageForm
from people.devs_dc_helpers import DevsDCAPIHelper
from people.models import Person
from storages.backends.s3boto3 import S3Boto3Storage


class ImageView(UpdateView):
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


class LatestLeaflets(ListView):
    model = Leaflet
    template_name = "leaflets/index.html"
    paginate_by = 60


class LeafletView(DetailView):
    template_name = "leaflets/leaflet.html"
    model = Leaflet

    def get_context_data(self, **kwargs):
        context = super(LeafletView, self).get_context_data(**kwargs)
        context["analysis_form"] = QuestionSetForm(
            self.object, self.request.user
        )

        context["person"] = self.object.get_person()
        context["party"] = self.object.get_party()
        context["ballot"] = self.object.get_ballot()

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


class LeafletUploadWizzard(NamedUrlSessionWizardView):
    extra_added = False
    file_storage = S3Boto3Storage()

    storage_name = "core.storage_helpers.PreUploadedSessionStorage"

    TEMPLATES = {
        "images": "leaflets/upload_form/images.html",
        "postcode": "leaflets/upload_form/postcode.html",
        "people": "leaflets/upload_form/people.html",
    }

    def get_template_names(self):
        step_name = self.steps.current
        return [self.TEMPLATES[step_name]]

    def get_form_initial(self, step):
        if step == "people":
            api = DevsDCAPIHelper()
            postcode = self.get_cleaned_data_for_step("postcode")
            if postcode:
                results = api.postcode_request(postcode["postcode"])
                if results.status_code == 200:
                    return {"postcode_results": results}
            return {}

    def get_context_data(self, **kwargs):
        context = super(LeafletUploadWizzard, self).get_context_data(**kwargs)
        context["hide_footer"] = True
        return context

    def get(self, *args, **kwargs):
        if "reset" in self.request.GET:
            self.storage.reset()
            return HttpResponseRedirect("/")
        return super(LeafletUploadWizzard, self).get(*args, **kwargs)

    def done(self, form_list, **kwargs):
        # Create a new leaflet
        leaflet = Leaflet()
        leaflet.save()
        for form in form_list:
            form_prefix = form.prefix.split("-")[0]
            if form_prefix in [
                "images",
            ]:
                # Dealing with an image form
                uploaded_images = self.storage.get_step_files("images").getlist(
                    "images-image"
                )
                for s3_file in uploaded_images:
                    image = LeafletImage(leaflet=leaflet)
                    image.image = s3_file
                    image.save()

            if form_prefix == "postcode":
                leaflet.postcode = form.cleaned_data["postcode"]

            if form_prefix == "people":
                if (
                    "people" in form.cleaned_data
                    and isinstance(form.cleaned_data["people"], str)
                    and form.cleaned_data["people"] != ""
                ):
                    signer = Signer()
                    data = json.loads(
                        signer.unsign(form.cleaned_data["people"])
                    )
                    leaflet.ynr_party_id = data["ynr_party_id"]
                    leaflet.ynr_party_name = data["ynr_party_name"]
                    leaflet.ballot_id = data["ballot_id"]

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

                    leaflet.publisher_person = person

                elif (
                    isinstance(form.cleaned_data["parties"], str)
                    and form.cleaned_data["parties"] != ""
                ):
                    signer = Signer()
                    (
                        leaflet.ynr_party_id,
                        leaflet.ynr_party_name,
                    ) = signer.unsign(form.cleaned_data["parties"]).split("--")

                else:
                    person = form.cleaned_data.get("people")
                    if person:
                        if person.current_party:
                            leaflet.publisher_party = person.current_party.party
                        leaflet.publisher_person = person
                        leaflet.election = person.current_election

        leaflet.save()
        messages.success(
            self.request, random.sample(settings.THANKYOU_MESSAGES, 1)[0]
        )

        return redirect(reverse("leaflet", kwargs={"pk": leaflet.pk}))
