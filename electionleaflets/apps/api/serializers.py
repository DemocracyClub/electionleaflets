from leaflets.models import Leaflet, LeafletImage
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail


class LeafletImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeafletImage
        fields = (
            "image",
            "image_type",
        )

    image = serializers.ImageField()


class LeafletSerializer(serializers.HyperlinkedModelSerializer):
    images = LeafletImageSerializer(many=True, required=False)
    party = serializers.SerializerMethodField()
    people = serializers.SerializerMethodField()
    first_page_thumb = serializers.SerializerMethodField()

    def get_party(self, obj: Leaflet):
        return {
            "party_id": obj.ynr_party_id,
            "party_name": obj.ynr_party_name,
        }

    def get_people(self, obj):
        people = []
        data = obj.people or {}
        for ynr_id, person_data in data.items():
            person_data["person"].pop("email", None)
            person_data["person"].pop("photo_url", None)
            people.append({ynr_id: person_data})
        return people

    def get_first_page_thumb(self, obj):
        image = obj.get_first_image()
        if not image:
            return None
        return get_thumbnail(obj.get_first_image().image, "350").url

    def validate(self, data):
        if not data.get("status") or not data.get("images"):
            data["status"] = "draft"
        return data

    class Meta:
        model = Leaflet
        depth = 1
        fields = (
            "pk",
            "title",
            "description",
            "party",
            "people",
            "images",
            "first_page_thumb",
            "date_uploaded",
            "date_delivered",
            "status",
        )


class LeafletMinSerializer(serializers.ModelSerializer):
    images = LeafletImageSerializer(many=True, required=False)
    first_page_thumb = serializers.SerializerMethodField()

    def get_first_page_thumb(self, obj):
        image = obj.get_first_image()
        if not image:
            return None
        return get_thumbnail(obj.get_first_image().image, "350").url

    class Meta:
        model = Leaflet
        depth = 0
        fields = (
            "pk",
            "title",
            "description",
            "publisher_party",
            "constituency",
            "images",
            "first_page_thumb",
            "date_uploaded",
            "date_delivered",
            "status",
            "ynr_person_id",
        )

    ynr_person_id = serializers.CharField(source="ynr_person_id")


class BallotSerializer(serializers.Serializer):
    ballot_id = serializers.CharField()
    count = serializers.IntegerField()
    url = serializers.HyperlinkedIdentityField(
        view_name="api:ballot-detail",
        lookup_field="ballot_id",
        lookup_url_kwarg="ballot_id",
    )
