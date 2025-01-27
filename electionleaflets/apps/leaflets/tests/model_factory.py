import factory
from factory.django import DjangoModelFactory
from leaflets.models import Leaflet


class LeafletFactory(DjangoModelFactory):
    class Meta:
        model = Leaflet

    title = factory.Sequence(lambda n: "Leaflet %d" % n)
    description = "test description"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # override auto_now_add for "date_uploaded" column
        date_uploaded = kwargs.pop("date_uploaded", None)
        obj = super()._create(model_class, *args, **kwargs)
        if date_uploaded is not None:
            model_class.objects.filter(id=obj.id).update(
                date_uploaded=date_uploaded
            )
        return obj
