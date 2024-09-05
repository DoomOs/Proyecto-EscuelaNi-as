# Generated by Django 5.0.6 on 2024-08-07 23:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("Curso", "0001_initial"),
        ("Persona", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AsignacionCiclo",
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
                ("year", models.IntegerField()),
                (
                    "alumna",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="Persona.alumna"
                    ),
                ),
                (
                    "grado",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="Curso.grado"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]