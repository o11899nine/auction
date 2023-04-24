# Generated by Django 4.2 on 2023-04-24 08:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0010_alter_listing_image_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
