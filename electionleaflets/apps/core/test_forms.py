import pytest

from electionleaflets.apps.core.forms import ReportAbuseForm


@pytest.mark.django_db
def test_form_valid_data():
    form = ReportAbuseForm(data={
        'name': 'Sam',  
        'details': 'This is not a spam leaflet.',
        'email': 'user@example.com',
    })
    assert form.is_valid()

@pytest.mark.django_db
def test_form_invalid_data():
    form = ReportAbuseForm(data={
        'name': '',  
        'details': 'This is a spam leaflet.',
        'email': 'user@example.com',
    })
    assert not form.is_valid()

@pytest.mark.django_db
def test_form_missing_data():
    form = ReportAbuseForm(data={
        'name': 'Sam',  
        'details': 'This is a spam leaflet.',
    })
    assert not form.is_valid()
 
