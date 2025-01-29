from leaflets.models import Leaflet

DUMMY_YNR_PERSON = {
    "123": {
        "party": {
            "url": "https://candidates.democracyclub.org.uk/api/next/parties/PP17545/",
            "name": "Party Of Women",
            "ec_id": "PP17545",
            "created": "2024-02-10T02:06:41.215363Z",
            "modified": "2024-06-10T03:06:39.655791+01:00",
            "legacy_slug": "party:17545",
        },
        "ballot": {
            "ballot_title": "UK Parliamentary general election: Sheffield Heeley",
            "ballot_paper_id": "parl.sheffield-heeley.2024-07-04",
        },
        "person": {
            "id": 117756,
            "url": "https://candidates.democracyclub.org.uk/api/next/people/117756/",
            "name": "Louise McDonald",
        },
        "result": None,
        "created": "2024-06-07T22:33:17.872125+01:00",
        "elected": None,
        "modified": "2024-06-07T22:33:17.874020+01:00",
        "deselected": False,
        "party_name": "Party Of Women",
        "deselected_source": None,
        "party_list_position": None,
        "party_description_text": "",
    }
}


def test_person_view(db, client):
    Leaflet.objects.create(
        title="Test Leaflet",
        description=None,
        ynr_party_id="party:1",
        ynr_party_name="Labour Party",
        person_ids=[123],
        people=DUMMY_YNR_PERSON,
    )

    resp = client.get("/person/123/")
    assert resp.status_code == 200

    resp = client.get("/person/321/")
    assert resp.status_code == 404
