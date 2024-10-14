import pytest
from analysis.models import (LeafletProperties, LeafletPropertiesManager,
                             LeafletPropertiesQuerySet)
from django.contrib.auth.models import User
from leaflets.models import Leaflet

@pytest.mark.django_db
class TestLeafletPropertiesQuerySet:
	@pytest.fixture(autouse=True)
	def setup(self):
		leaflet = Leaflet.objects.create()	
		user = User.objects.create(username=f"test_user")
		LeafletProperties.objects.create(leaflet=leaflet, key="has_leader_photo", value="Yes", user=user)
		LeafletProperties.objects.create(leaflet=leaflet, key="has_opposition_leader", value="Yes", user=user)
		LeafletProperties.objects.create(leaflet=leaflet, key="has_leader", value="Yes", user=user)
		LeafletProperties.objects.create(leaflet=leaflet, key="squeeze_message", value="Yes", user=user)
		LeafletProperties.objects.create(leaflet=leaflet, key="has_opposition_leader_photo", value="Yes", user=user)
		LeafletProperties.objects.create(leaflet=leaflet, key="leaflet_style", value="leaflet_type", user=user)
		LeafletProperties.objects.create(leaflet=leaflet, key="has_logo", value="Yes", user=user)
		LeafletProperties.objects.create(leaflet=leaflet, key="include_graph", value="Yes", user=user)
		LeafletProperties.objects.create(leaflet=leaflet, key="leaflet_style", value="leaflet_type", user=user)
		self.qs = LeafletProperties.objects.all()
		
	def test_leaders_photo_count(self):
		assert self.qs.leaders_photo_count() == 1	

	def test_opposition_photo_count(self):
		assert self.qs.opposition_photo_count() == 1
	
	def test_leaders_mentions(self):
		assert self.qs.leaders_mentions() == 1
	
	def test_squeeze_messages_count(self):
		assert self.qs.squeeze_messages_count() == 1
	
	def test_opposition_mentions_count(self):
		assert self.qs.opposition_mentions_count() == 1

	def test_leaflet_type_count(self):
		assert self.qs.leaflet_type_count("leaflet_type") == 2
	
	def test_party_logo(self):
		assert self.qs.party_logo() == 1

	def test_graphs_count(self):
		assert self.qs.graphs_count() == 1

	def test_leaflets_analysed(self):
		assert self.qs.leaflets_analysed() == 1 
  
@pytest.mark.django_db
class TestLeafletPropertiesManager:	
	def test_get_queryset(self):
		manager = LeafletProperties.objects
		assert isinstance(manager.get_queryset(), LeafletPropertiesQuerySet)