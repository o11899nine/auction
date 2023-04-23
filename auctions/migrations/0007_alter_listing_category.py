# Generated by Django 4.2 on 2023-04-23 11:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0006_alter_listing_image_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="category",
            field=models.CharField(
                choices=[
                    ("Toys", "Toys"),
                    ("Cars", "Cars"),
                    ("Clothing", "Clothing"),
                    ("Furniture", "Furniture"),
                    ("Instruments", "Instruments"),
                ],
                max_length=64,
            ),
        ),
    ]