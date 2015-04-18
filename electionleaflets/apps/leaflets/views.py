import os
import random
from collections import OrderedDict
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.formtools.wizard.views import NamedUrlSessionWizardView
from django.core.urlresolvers import reverse
from django.conf import settings
from django.views.generic import (DetailView, ListView, UpdateView, FormView,
                                    RedirectView)
from django.views.generic.detail import BaseDetailView, SingleObjectMixin
from django.core.files.storage import FileSystemStorage
from braces.views import StaffuserRequiredMixin

from core.helpers import geocode
from people.models import Person
from .models import Leaflet, LeafletImage
from .forms import (InsidePageImageForm, LeafletDetailsFrom,
    LeafletReviewFrom)


class ImageView(DetailView):
    model = LeafletImage
    template_name = 'leaflets/full.html'

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
    template_name = 'leaflets/full_all.html'


class ImageRotateView(StaffuserRequiredMixin, DetailView):
    model = LeafletImage
    template_name = 'leaflets/image_rotate.html'
    def post(self, request, *args, **kwargs):
        image_model = self.get_object()
        rotation = request.POST.get('rotate')
        print rotation
        image_model.rotate(int(rotation))
        return HttpResponseRedirect(image_model.get_absolute_url())




class ImageCropView(StaffuserRequiredMixin, DetailView):
    model = LeafletImage
    template_name = 'leaflets/image_crop.html'

    def post(self, request, *args, **kwargs):
        image_model = self.get_object()
        x = int(request.POST.get('x'))
        y = int(request.POST.get('y'))
        x2 = int(request.POST.get('x2'))
        y2 = int(request.POST.get('y2'))

        image_model.crop(x, y, x2, y2)
        return HttpResponseRedirect(image_model.get_absolute_url())


class LatestLeaflets(ListView):
    model = Leaflet
    template_name = 'leaflets/index.html'
    paginate_by = 60


class LeafletView(UpdateView):
    template_name = 'leaflets/leaflet.html'
    model = Leaflet
    form_class = LeafletReviewFrom

    def get_success_url(self):
        if 'submit_and_next' in self.request.POST:
            next_models = Leaflet.objects.filter(reviewed=False)\
                                .order_by('-date_uploaded')
            if next_models:
                return next_models[0].get_absolute_url()
            else:
                return '/'
        return super(LeafletView, self).get_success_url()

def _skip_step_allowed_condition(wizard, step_name):
    extra_data = wizard.storage.extra_data
    if 'skip_to_postcode' in extra_data and extra_data['skip_to_postcode']:
        must_use = True
        # cleaned_data = wizard.get_cleaned_data_for_step('front') or {}
        # if cleaned_data.get('image'):
        #     must_use = True

        cleaned_data = wizard.get_cleaned_data_for_step(step_name) or {}
        if cleaned_data.get('image'):
            must_use = True
        else:
            must_use = False
        return must_use
    return True


def skip_back_allowed(wizard):
    return _skip_step_allowed_condition(wizard, 'back')


def skip_inside_allowed(wizard):
    return _skip_step_allowed_condition(wizard, 'inside')


class LeafletUploadWizzard(NamedUrlSessionWizardView):
    extra_added = False

    TEMPLATES = {
        "front": "leaflets/upload_form/image_front.html",
        "back": "leaflets/upload_form/image_back.html",
        "inside": "leaflets/upload_form/image_inside.html",
        "postcode": "leaflets/upload_form/postcode.html",
        "people": "leaflets/upload_form/people.html",
    }

    file_storage = FileSystemStorage(location=os.path.join(
        settings.MEDIA_ROOT, 'images/leaflets_tmp'))

    def get_template_names(self):
            if self.steps.current.startswith('inside'):
                step_name = 'inside'
            else:
                step_name = self.steps.current
            return [self.TEMPLATES[step_name]]

    def get_form_initial(self, step):
        if step == "people":
            # self.get_cleaned_data_for_step('postcode')['postcode']
            geo_data = self.get_cleaned_data_for_step('postcode')
            people_qs = Person.objects.filter(
                personconstituencies__constituency=geo_data['constituency'])

            return {
                '_people': people_qs
            }
        return {}


    @property
    def extra_inside_forms(self):
        return self.storage.extra_data.get('extra_inside', 0)


    def get_context_data(self, **kwargs):
        context = super(LeafletUploadWizzard, self).get_context_data(**kwargs)
        context['hide_footer'] = True
        return context

    def add_extra_inside_forms(self):
        self.storage.extra_data['extra_inside'] = self.extra_inside_forms + 1
        self.extra_added = True

    def get(self, *args, **kwargs):
        self._insert_extra_inside_forms()
        return super(LeafletUploadWizzard, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        if self.request.POST.get('cancel_upload', None):
            self.storage.reset()
            return HttpResponseRedirect(reverse('home'))
        if self.request.POST.get('skip', None):
            self.storage.extra_data['skip_to_postcode'] = True
            return self.render_goto_step('postcode')

        self._insert_extra_inside_forms()

        if self.request.POST.get('add_extra_inside', None):
            form = self.get_form(
                data=self.request.POST, files=self.request.FILES)
            if form.is_valid():
                self.add_extra_inside_forms()
                self._insert_extra_inside_forms(force=True)
        return super(LeafletUploadWizzard, self).post(*args, **kwargs)

    def _insert_extra_inside_forms(self, force=False):
        """
        Adds to self.form_list, inserting an extra 'inside page' form
        after the last inside page form we have.
        """
        if not self.extra_inside_forms:
            return self.form_list
        if self.extra_added and not force:
            return self.form_list
        form_list = [(k, v) for k, v in self.form_list.items()]
        form_list.reverse()
        for index, (name, form) in enumerate(form_list):
            if name.startswith('inside'):
                for step in range(self.extra_inside_forms):
                    new_name = "inside-%s" % step
                    form_list.insert(index, (new_name, InsidePageImageForm))
                break
        form_list.reverse()
        self.form_list = OrderedDict()
        for k, v in form_list:
            self.form_list[k] = v
        self.extra_added = True
        return self.form_list

    def done(self, form_list, **kwargs):
        #Create a new leaflet
        leaflet = Leaflet()
        leaflet.save()
        for form in form_list:
            form_prefix = form.prefix.split('-')[0]
            if form_prefix in ['front', 'back', 'inside']:
                # Dealing with an image form
                image_type = None
                if form.prefix == "front":
                    image_type = "1_front"
                if form.prefix == "back":
                    image_type = "2_back"
                if form.prefix == "inside":
                    image_type = "3_inside"
                image = LeafletImage(leaflet=leaflet, image_type=image_type)
                image.image = form.cleaned_data['image']
                image.save()

            if form_prefix == "postcode":
                leaflet.postcode = form.cleaned_data['postcode']

            if form_prefix == "people":
                person = form.cleaned_data['people']
                if person:
                    leaflet.publisher_party = person.current_party.party
                    leaflet.publisher_person = person
                    leaflet.election = person.current_election

        leaflet.save()
        messages.success(self.request, random.sample(settings.THANKYOU_MESSAGES, 1)[0])

        return  redirect(reverse('leaflet', kwargs={'pk': leaflet.pk}))
