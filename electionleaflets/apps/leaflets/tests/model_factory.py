import factory
from factory.django import DjangoModelFactory
from leaflets.models import Leaflet


class LeafletFactory(DjangoModelFactory):
    class Meta:
        model = Leaflet

    title = factory.Sequence(lambda n: "Leaflet %d" % n)
    description = "test description"
    ballots = [
        {
            "election_id": "parl.2024-07-04",
            "ballot_title": "UK Parliamentary general election: Newbury",
            "election_name": "UK Parliamentary general election",
            "ballot_paper_id": "parl.newbury.2024-07-04",
        }
    ]

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
