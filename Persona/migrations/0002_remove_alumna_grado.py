# Generated by Django 5.0.6 on 2024-08-15 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Persona", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="alumna",
            name="grado",
        ),
    ]
