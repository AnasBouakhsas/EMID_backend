# Generated by Django 5.0.4 on 2024-07-10 15:04

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_remove_clients_id_alter_client_discounts_stamp_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="clients",
            name="Allow_Check",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="clients",
            name="Allow_PDC",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="clients",
            name="Area_Of_Business_Code",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="clients",
            name="Channel_Code",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="clients",
            name="City_Code",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="clients",
            name="Classification_Code",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="clients",
            name="Client_Type_ID",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="clients",
            name="Collection_Type",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="clients",
            name="Currency_Code",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="clients",
            name="Fax_Number",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="clients",
            name="Grace_Period",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="clients",
            name="Invoice_Limit",
            field=models.DecimalField(
                blank=True, decimal_places=6, max_digits=18, null=True
            ),
        ),
        migrations.AddField(
            model_name="clients",
            name="Invoice_Settlement",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="clients",
            name="IsFromERP",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="clients",
            name="Is_Dummy",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="clients",
            name="Is_From_Census",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="clients",
            name="Is_Taxable",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="clients",
            name="Latitude",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="clients",
            name="Longitude",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="clients",
            name="Number_Of_Outlets",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="clients",
            name="Org_ID",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="clients",
            name="Parent_Client_Code",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="clients",
            name="Price_List_Code",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="clients",
            name="Price_List_Code2",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="clients",
            name="Region_Code",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.regions",
            ),
        ),
        migrations.AddField(
            model_name="clients",
            name="Return_Price_List_Code",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="clients",
            name="Sq_Meter_Area",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="clients",
            name="Stamp_Date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="clients",
            name="Tax_Code",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="clients",
            name="User_Code",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="client_discounts",
            name="Stamp_Date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 7, 10, 15, 4, 43, 564237, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="clients",
            name="Address",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="clients",
            name="Alt_Address",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="clients",
            name="Area_Code",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="clients",
            name="Barcode",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="clients",
            name="Client_Alt_Description",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="clients",
            name="Client_Description",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="clients",
            name="Client_Status_ID",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="clients",
            name="Contact_Person",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="clients",
            name="Payment_Term_Code",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="clients",
            name="Phone_Number",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterModelTable(
            name="clients",
            table=None,
        ),
    ]
