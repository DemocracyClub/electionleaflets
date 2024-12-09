from leaflets.models import Leaflet


def test_person_view(db, client):
    Leaflet.objects.create(
        title="Test Leaflet",
        description=None,
        ynr_party_id="party:1",
        ynr_party_name="Labour Party",
        person_ids=[123],
    )

    resp = client.get("/person/123/")
    assert resp.status_code == 200

    resp = client.get("/person/321/")
    assert resp.status_code == 404
