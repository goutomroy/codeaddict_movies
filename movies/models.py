from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_extensions.db.fields import AutoSlugField

from core.models import BaseModel


class Movie(BaseModel):
    default_number_of_tickets = 10

    name = models.CharField(max_length=256)
    slug = AutoSlugField(populate_from=["name"])
    ticket_price = models.FloatField(validators=[MinValueValidator(1.0)])
    number_of_tickets = models.PositiveSmallIntegerField(
        default=default_number_of_tickets
    )
    rating = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(10.0)], default=1.0
    )

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.name
