# Generated by Django 4.2.2 on 2025-01-31 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("restaurants", "0001_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="table",
            unique_together={("number", "restaurant")},
        ),
    ]
