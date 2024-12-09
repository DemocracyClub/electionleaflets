from leaflets.models import Leaflet


def test_party_page_status_codes(db, client):
    assert client.get("/parties/ppxxx/none").status_code == 404

    Leaflet.objects.create(ynr_party_id="PP123")
    assert client.get("/parties/PP123/none").status_code == 200


def test_party_list_page(db, client):
    Leaflet.objects.create(ynr_party_id="PP123", ynr_party_name="Test")
    assert client.get("/parties/").status_code == 200
