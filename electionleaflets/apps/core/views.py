# -*- coding: utf-8 -*-
from django.template  import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import FormView, TemplateView, DetailView
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from constituencies.forms import ConstituencyLookupForm
from leaflets.models import Leaflet
from .helpers import geocode
from .forms import ReportAbuseForm
import datetime
from core.helpers import geocode

class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):

        #get leaflet count
        start_date = datetime.date(2015, 1, 1)
        leaflet_count = Leaflet.objects.filter(date_uploaded__gt=start_date).count()
        context = super(HomeView, self).get_context_data(**kwargs)

        #get latest leaflets (with titles)
        latest_leaflets = Leaflet.objects.all()[:9]

        #update context
        context.update({'leaflet_count': leaflet_count, 'start_date': start_date, 'latest_leaflets': latest_leaflets})


        return context

class MaintenanceView(TemplateView):
    template_name = "core/maintenance.html"


class ReportView(DetailView, FormView):
    model = Leaflet
    form_class = ReportAbuseForm
    template_name = "core/report_abuse.html"

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.object = self.get_object()
        context = self.get_context_data(
            form=form,
            object=self.object,
        )
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return super(ReportView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        domain = Site.objects.get_current().domain
        ctx = {
            'link': 'http://%s%s' % (
                domain, reverse('leaflet', kwargs={
                        'pk':self.object.id
                    }),
            ),
            'name': form.cleaned_data['name'],
            'email': form.cleaned_data['email'],
            'details': form.cleaned_data['details'],
        }

        subject = "{0} – {1}".format(
            settings.REPORT_EMAIL_SUBJECT,
            self.object.id
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        to = settings.EMAIL_RECIPIENT

        text_content = render_to_string('email/abuse_report.txt', ctx)
        html_content = render_to_string('email/abuse_report.html', ctx)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return HttpResponseRedirect(
            reverse('report_abuse_sent', kwargs={'pk': self.object.pk})
        )

class ReportThanksView(DetailView):
    model = Leaflet
    template_name = "core/report_sent.html"
