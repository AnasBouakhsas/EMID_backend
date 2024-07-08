# Generated by Django 5.0.4 on 2024-07-08 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_client_discounts_month_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="channels",
            name="delivery_system",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="channels",
            name="related_price_list_code",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="channels",
            name="return_price_list_code",
            field=models.CharField(max_length=50, null=True),
        ),
    ]
