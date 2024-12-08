# -*- coding: utf-8 -*-

from constituencies.models import Constituency
from django.urls import reverse
from django.views.generic import TemplateView
from leaflets.models import Leaflet, LeafletImage
from people.models import Person
from uk_political_parties.models import Party

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
