# Generated by Django 5.0.6 on 2024-08-08 21:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("Asignacion_Ciclo", "0001_initial"),
        ("Curso", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Actividad",
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
                ("actividad", models.CharField(max_length=100)),
                ("punteo", models.IntegerField()),
                ("fecha", models.DateField(auto_now_add=True)),
                (
                    "curso",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="Curso.curso"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CalificacionActividad",
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
                ("descripcion", models.CharField(max_length=100, null=True)),
                ("punteo", models.IntegerField()),
                (
                    "actividad",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Actividad.actividad",
                    ),
                ),
                (
                    "asignacion_ciclo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Asignacion_Ciclo.asignacionciclo",
                    ),
                ),
            ],
            options={
                "unique_together": {("actividad", "asignacion_ciclo")},
            },
        ),
    ]