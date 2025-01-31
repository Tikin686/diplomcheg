# Generated by Django 4.2.2 on 2025-01-31 14:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurants", "0005_rename_client_feedback_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedback",
            name="restaurant",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="restaurant",
                to="restaurants.restaurant",
            ),
        ),
    ]
