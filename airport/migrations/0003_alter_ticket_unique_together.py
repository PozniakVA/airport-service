# Generated by Django 5.1 on 2024-08-27 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("airport", "0002_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="ticket",
            unique_together={("row", "seat")},
        ),
    ]
