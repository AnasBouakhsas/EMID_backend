# Generated by Django 5.0.4 on 2024-07-31 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0013_alter_promoitembasketheaders_last_updated_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="promoitembasketheaders",
            name="products",
            field=models.ManyToManyField(
                blank=True, related_name="baskets", to="users.produit"
            ),
        ),
    ]
