# Generated by Django 2.2.20 on 2021-05-02 12:55

from django.db import migrations


def change_ballot_data_structure(apps, schema_editor):
    Leaflet = apps.get_model("leaflets", "Leaflet")
    qs = Leaflet.objects.exclude(ballots=[])
    for leaflet in qs:
        new_ballots = []
        for ballot in leaflet.ballots:
            if isinstance(ballot, dict):
                new_ballots.append(ballot)
                continue
            ballot_dict = {
                "ballot_paper_id": ballot,
                "ballot_title": ballot,
            }
            new_ballots.append(ballot_dict)
        leaflet.ballots = new_ballots
        leaflet.save()


class Migration(migrations.Migration):

    dependencies = [
        ("leaflets", "0003_auto_20210501_1655"),
    ]

    operations = [migrations.RunPython(change_ballot_data_structure)]
