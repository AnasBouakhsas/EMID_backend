# Generated by Django 5.0.4 on 2024-08-08 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0019_remove_promoheaders_clients_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Client_Statut",
        ),
        migrations.DeleteModel(
            name="UserGroupe",
        ),
    ]
