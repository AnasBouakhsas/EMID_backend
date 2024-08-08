# Generated by Django 5.0.4 on 2024-08-08 13:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0020_delete_client_statut_delete_usergroupe"),
    ]

    operations = [
        migrations.CreateModel(
            name="Client_Statut",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "Client_Statut_ID",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(2),
                        ]
                    ),
                ),
                ("Statut_Description", models.CharField(max_length=50)),
            ],
            options={
                "db_table": "Client_Statut",
            },
        ),
    ]
