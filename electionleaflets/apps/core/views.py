# -*- coding: utf-8 -*-
import datetime

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.cache import cache_control
from django.views.generic import FormView, TemplateView, DetailView
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from constituencies.models import Constituency
from leaflets.models import Leaflet, LeafletImage
from people.models import Person
from uk_political_parties.models import Party

from .forms import ReportAbuseForm
from .helpers import CacheControlMixin


class HomeView(CacheControlMixin, TemplateView):
    template_name = "core/home.html"
    cache_timeout = 60 * 5

    def get_context_data(self, **kwargs):

        leaflet_count = Leaflet.objects.all().count()
        context = super(HomeView, self).get_context_data(**kwargs)

        # get the latest leaflets (with titles)
        latest_leaflets = Leaflet.objects.all().prefetch_related("images")[:20]

        # update context
        context.update(
            {
                "leaflet_count": leaflet_count,
                "latest_leaflets": latest_leaflets,
            }
        )

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
        context = self.get_context_data(form=form, object=self.object,)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ReportView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        domain = Site.objects.get_current().domain
        ctx = {
            "link": "http://%s%s"
            % (domain, reverse("leaflet", kwargs={"pk": self.object.id}),),
            "name": form.cleaned_data["name"],
            "email": form.cleaned_data["email"],
            "details": form.cleaned_data["details"],
        }

        subject = "{0} – {1}".format(
            settings.REPORT_EMAIL_SUBJECT, self.object.id
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        to = settings.EMAIL_RECIPIENT

        text_content = render_to_string("email/abuse_report.txt", ctx)
        html_content = render_to_string("email/abuse_report.html", ctx)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return HttpResponseRedirect(
            reverse("report_abuse_sent", kwargs={"pk": self.object.pk})
        )


class ReportThanksView(DetailView):
    model = Leaflet
    template_name = "core/report_sent.html"


class TestView(TemplateView):
    template_name = "core/test.html"

    def get_context_data(self, **kwargs):
        links = []

        links.append({"text": "Home", "url": reverse("home")})
        links.append({"text": "About", "url": reverse("about")})

        links.append({"text": "Analysis", "url": reverse("analysis")})
        links.append(
            {"text": "Analysis Reports", "url": reverse("report_view")}
        )
        links.append(
            {"text": "Analysis in total", "url": reverse("analysis_report")}
        )
        links.append(
            {
                "text": "Analysis per party",
                "url": reverse("analysis_report_per_party"),
            }
        )
        links.append(
            {
                "text": "Analysis per constituency",
                "url": reverse("constituencies_report"),
            }
        )
        links.append(
            {
                "text": "Start Analysis",
                "url": reverse("analysis_start"),
                "help": "should redirect to a random un-analysed leaflet",
            }
        )

        links.append(
            {"text": "Constituencies", "url": reverse("constituencies_report")}
        )
        constituency = Constituency.objects.order_by("?").first()
        links.append(
            {
                "text": "Constituency view",
                "url": reverse(
                    "constituency-view", kwargs={"pk": constituency.pk}
                ),
            }
        )

        links.append(
            {
                "text": "Donate",
                "url": "/donate",
                "help": "should redirect to /donate on DC website",
            }
        )

        leaflet = Leaflet.objects.order_by("?").first()
        image = LeafletImage.objects.order_by("?").first()
        links.append({"text": "Latest leaflets", "url": reverse("leaflets")})
        links.append(
            {
                "text": "Leaflet view",
                "url": reverse("leaflet", kwargs={"pk": leaflet.pk}),
            }
        )
        links.append(
            {
                "text": "Leaflet images",
                "url": reverse("all_images", kwargs={"pk": leaflet.pk}),
            }
        )
        links.append(
            {
                "text": "Full leaflet image",
                "url": reverse("full_image", kwargs={"pk": image.pk}),
            }
        )
        links.append({"text": "Add leaflet", "url": reverse("upload_leaflet")})
        links.append(
            {
                "text": "Report a leaflet",
                "url": reverse("report_abuse", kwargs={"pk": leaflet.pk}),
            }
        )
        links.append(
            {
                "text": "Report a leaflet - thanks",
                "url": reverse("report_abuse_sent", kwargs={"pk": leaflet.pk}),
            }
        )

        party = Party.objects.order_by("?").first()
        links.append({"text": "Parties", "url": reverse("parties")})
        links.append(
            {
                "text": "Party view",
                "url": reverse("party-view", kwargs={"pk": party.pk}),
            }
        )

        person = Person.objects.order_by("?").first()
        links.append(
            {
                "text": "Person view",
                "url": reverse("person", kwargs={"remote_id": person.pk}),
            }
        )

        links.append({"text": "Press", "url": reverse("press")})

        context = super(TestView, self).get_context_data(**kwargs)

        context.update({"links": links})
        return context
