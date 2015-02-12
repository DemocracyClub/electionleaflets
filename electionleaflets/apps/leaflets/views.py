import os
from collections import OrderedDict

from django.template  import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import NamedUrlSessionWizardView
from django.core.urlresolvers import reverse
from django.conf import settings
from django.views.generic import DetailView, ListView
from django.core.files.storage import FileSystemStorage

from .models import Leaflet, LeafletImage
from .forms import InsidePageImageForm

class ImageView(DetailView):
    model = LeafletImage
    template_name = 'leaflets/full.html'
    pk_url_kwarg = 'image_key'

def view_all_full_images(request, leafletid):
    from leaflets.models import Leaflet, LeafletImage

    leaflet = get_object_or_404(Leaflet, pk=leafletid)
    images = LeafletImage.objects.filter(leaflet=leaflet)

    return render_to_response('leaflets/full_all.html',
                            {
                                'images': images,
                                'leaflet': leaflet,
                            },
                            context_instance=RequestContext(request), )


class LatestLeaflets(ListView):
    model = Leaflet
    template_name = 'leaflets/index.html'
    paginate_by = 60


class LeafletView(DetailView):
    template_name = 'leaflets/leaflet.html'
    queryset = Leaflet.objects.all()


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
    }

    file_storage = FileSystemStorage(location=os.path.join(
        settings.MEDIA_ROOT, 'images/leaflets_tmp'))

    def get_template_names(self):
            if self.steps.current.startswith('inside'):
                step_name = 'inside'
            else:
                step_name = self.steps.current
            return [self.TEMPLATES[step_name]]

    @property
    def extra_inside_forms(self):
        return self.storage.extra_data.get('extra_inside', 0)

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
            form = self.get_form(data=self.request.POST, files=self.request.FILES)
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
        form_list = [(k,v) for k,v in self.form_list.items()]
        form_list.reverse()
        for index, (name,form) in enumerate(form_list):
            if name.startswith('inside'):
                for step in range(self.extra_inside_forms):
                    new_name = "inside-%s" % step
                    form_list.insert(index, (new_name, InsidePageImageForm))
                break
        form_list.reverse()
        self.form_list = OrderedDict()
        for k,v in form_list:
            self.form_list[k] = v
        self.extra_added = True
        return self.form_list

    def done(self, form_list, **kwargs):
        #Create a new leaflet
        leaflet = Leaflet()
        leaflet.save()

        import ipdb
        # ipdb.set_trace()

        for form in form_list:
            if form.prefix.split('-')[0] in ['front', 'back', 'inside']:
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

        # Front

        return  redirect(reverse('leaflet', kwargs={'pk': leaflet.pk}))
