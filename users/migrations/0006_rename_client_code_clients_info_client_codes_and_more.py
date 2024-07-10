# Generated by Django 5.0.4 on 2024-07-10 15:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_remove_clients_allow_check_remove_clients_allow_pdc_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="clients_info",
            old_name="Client_Code",
            new_name="Client_Codes",
        ),
        migrations.AlterField(
            model_name="client_discounts",
            name="Stamp_Date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 7, 10, 15, 40, 2, 402848, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
