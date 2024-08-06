# Generated by Django 5.0.4 on 2024-07-31 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0010_device"),
    ]

    operations = [
        migrations.CreateModel(
            name="Produit",
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
                ("CodeProduit", models.CharField(max_length=100, unique=True)),
                ("ProduitDescription", models.CharField(max_length=100)),
                ("AltProduitDescription", models.CharField(max_length=100)),
                ("typeProduit", models.CharField(default="Item", max_length=100)),
            ],
        ),
    ]