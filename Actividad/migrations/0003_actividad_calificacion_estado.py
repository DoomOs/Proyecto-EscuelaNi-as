# Generated by Django 5.0.6 on 2024-10-16 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Actividad", "0002_actividad_estado"),
    ]

    operations = [
        migrations.AddField(
            model_name="actividad",
            name="calificacion_estado",
            field=models.IntegerField(default=0),
        ),
    ]