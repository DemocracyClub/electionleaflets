from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from leaflets.models import Leaflet, LeafletImage
from constituencies.models import Constituency
from uk_political_parties.models import Party
from people.models import Person


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

class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = (
            'pk',
            'name',
            'remote_id',
            'source_name',
            'source_url',
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
    publisher_person = PersonSerializer(required=False)
    first_page_thumb = serializers.SerializerMethodField()

    def get_first_page_thumb(self, obj):
        image = obj.get_first_image()
        if image:
            return get_thumbnail(obj.get_first_image().image, '350').url

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
            'publisher_person',
            'constituency',
            'images',
            'first_page_thumb',
            'date_uploaded',
            'date_delivered',
            'status',
        )
