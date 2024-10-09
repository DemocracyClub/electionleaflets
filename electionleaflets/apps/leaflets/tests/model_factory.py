import factory
from factory.django import DjangoModelFactory

from leaflets.models import Leaflet


class LeafletFactory(DjangoModelFactory):
    class Meta:
        model = Leaflet

    title = factory.Sequence(lambda n: "Leaflet %d" % n)
    description = "test description"
