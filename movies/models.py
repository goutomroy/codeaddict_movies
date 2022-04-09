import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from django_extensions.db.fields import AutoSlugField

from users.models import User


class BaseModel(models.Model):

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


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


class MovieTicket(BaseModel):

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created"]
        default_related_name = "tickets"
        constraints = [
            UniqueConstraint(
                name="%(app_label)s_%(class)s_unique_user_movie",
                fields=["movie", "user"],
            ),
        ]

    @staticmethod
    def has_read_permission(request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_read_permission(self, request):
        if self.user == request.user:
            return True
        return False

    def __str__(self):
        return self.movie.name + " " + self.user.email
