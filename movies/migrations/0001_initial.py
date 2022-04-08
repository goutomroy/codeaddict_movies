# Generated by Django 4.0.3 on 2022-04-08 19:55

import uuid

import django.core.validators
import django_extensions.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Movie",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=256)),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(
                        blank=True, editable=False, populate_from=["name"]
                    ),
                ),
                (
                    "ticket_price",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(1.0)]
                    ),
                ),
                ("number_of_tickets", models.PositiveSmallIntegerField(default=10)),
                (
                    "rating",
                    models.FloatField(
                        default=1.0,
                        validators=[
                            django.core.validators.MinValueValidator(1.0),
                            django.core.validators.MaxValueValidator(10.0),
                        ],
                    ),
                ),
            ],
            options={
                "ordering": ["-created"],
            },
        ),
    ]
