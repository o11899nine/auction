# Generated by Django 4.2 on 2023-04-28 09:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0017_listing_highest_bid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="highest_bid",
            field=models.FloatField(
                default=models.FloatField(
                    validators=[
                        django.core.validators.MinValueValidator(0),
                        django.core.validators.MaxValueValidator(1000000),
                    ]
                ),
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(1000000),
                ],
            ),
        ),
    ]
