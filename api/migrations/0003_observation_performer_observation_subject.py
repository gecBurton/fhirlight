# Generated by Django 5.1.4 on 2024-12-31 11:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_load_concepts"),
    ]

    operations = [
        migrations.AddField(
            model_name="observation",
            name="performer",
            field=models.ForeignKey(
                blank=True,
                help_text="Who is responsible for the observation",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="api.organization",
            ),
        ),
        migrations.AddField(
            model_name="observation",
            name="subject",
            field=models.ForeignKey(
                blank=True,
                help_text="Who and/or what the observation is about",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="api.patient",
            ),
        ),
    ]