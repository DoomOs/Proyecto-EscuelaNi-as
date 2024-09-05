# Generated by Django 5.0.6 on 2024-08-07 23:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Grado",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre_grado", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Curso",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre_curso", models.CharField(max_length=100)),
                (
                    "grado",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="Curso.grado"
                    ),
                ),
            ],
        ),
    ]