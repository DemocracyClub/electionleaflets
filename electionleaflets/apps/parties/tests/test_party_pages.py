from leaflets.models import Leaflet


def test_party_page_status_codes(db, client):
    assert client.get("/parties/ppxxx/none").status_code == 404

    Leaflet.objects.create(ynr_party_id="PP123")
    assert client.get("/parties/PP123/none").status_code == 200