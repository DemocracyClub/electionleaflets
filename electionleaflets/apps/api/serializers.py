from leaflets.models import Leaflet, LeafletImage
from constituencies.models import Constituency
from uk_political_parties.models import Party

from rest_framework import serializers


class ConstituencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Constituency
        fields = (
            'pk',
            'name',
            'country_name',
            'slug',
        )


class PartySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Party
        fields = (
            'pk',
            'party_name',
            'party_type',
            'status',
        )


class LeafletImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeafletImage
        fields = (
            'image',
            'image_text',
        )
    image = serializers.ImageField()


class LeafletSerializer(serializers.HyperlinkedModelSerializer):
    images = LeafletImageSerializer(many=True, required=False)
    constituency = ConstituencySerializer(required=False)
    publisher_party = PartySerializer(required=False)

    def validate(self, data):
        if not data.get('status') or not data.get('images'):
            data['status'] = 'draft'
        return data



    class Meta:
        model = Leaflet
        depth = 1
        fields = (
            'pk',
            'title',
            'description',
            'publisher_party',
            'constituency',
            'images',
            'date_uploaded',
            'date_delivered',
            'status',
        )
