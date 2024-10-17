import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from analysis.views import AnalysisStartRedirectView, BaseAnalysisReportView, ReportView, ReportViewMixin
from leaflets.models import Leaflet


import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from analysis.views import AnalysisStartRedirectView, BaseAnalysisReportView, ReportView
from leaflets.models import Leaflet


@pytest.fixture(autouse=True)
def setup_client():
	client = Client()
	User.objects.create_user(username='testuser', password='12345')
	client.login(username='testuser', password='12345')
	return client


@pytest.mark.django_db
class TestAnalysisHomeView:
	def test_analysis_home_view(self, setup_client):
		url = reverse('analysis')
		response = setup_client.get(url)
		assert response.status_code == 200
		assert 'contributing_people' in response.context
		assert 'total_contributions' in response.context
		assert 'number_of_people' in response.context
		assert 'leaflets_analysed' in response.context


@pytest.mark.django_db
class TestAnalysisStartRedirectView:
	def test_get_redirect_url(self, setup_client):
		Leaflet.objects.create()
		url = reverse('analysis_start')
		response = setup_client.get(url)
		assert response.status_code == 302
		view = AnalysisStartRedirectView()
		view.request = response.wsgi_request
		assert response.url == view.get_redirect_url()


@pytest.mark.django_db
class TestReportViewMixin:
	def setup(self):
		self.client = setup_client()
		Leaflet.objects.create()

	def test_leaflet_count(self):
		view = ReportView()
		assert view.leaflet_count == 0
		Leaflet.objects.create()
		assert view.leaflet_count == 1


@pytest.mark.django_db
class TestReportView:
	def test_get_context_data(self, setup_client):
		url = reverse('report_view')
		response = setup_client.get(url)
		assert response.status_code == 200
		view = ReportView()
		assert 'start_date' in view.get_context_data()
		assert 'leaflet_count' in view.get_context_data()


@pytest.mark.django_db
class TestConstituencyReportView:
	def test_constituency_report_view(self, setup_client):
		url = reverse('constituencies_report')
		response = setup_client.get(url)
		assert response.status_code == 200
		assert 'per_constituency' in response.context


@pytest.mark.django_db
class TestAnalysisReportView:
	def test_analysis_report_view(self, setup_client):
		url = reverse('analysis_report')
		response = setup_client.get(url)
		assert response.status_code == 200
@pytest.mark.django_db
class TestAnalysisPerPartyReportView:
	def test_analysis_per_party_report_view(self, setup_client):
		url = reverse('analysis_report_per_party')
		response = setup_client.get(url)
		assert response.status_code == 200
		assert 'parties' in response.context
  
@pytest.mark.django_db
class AnalysisPerPartyReportView():
    def test_get_context_data(self):
        view = AnalysisPerPartyReportView()
        context = view.get_context_data()
        assert 'parties' in context
        assert 'leaflet_count' in context
        assert 'leaders_photo_count' in context
        assert 'leaders_mentions' in context
        assert 'party_logo' in context
        assert 'opposition_photo_count' in context
        assert 'opposition_mentions_count' in context
	