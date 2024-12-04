# Generated by Django 4.2.16 on 2024-12-04 17:40

from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("leaflets", "0006_move_party_model_to_ynr_party"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="leaflet",
            name="publisher_party",
        ),
        migrations.AlterField(
            model_name="leafletimage",
            name="image",
            field=sorl.thumbnail.fields.ImageField(
                max_length=255, upload_to=""
            ),
        ),
    ]
