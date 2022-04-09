from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from movies.models import Movie, MovieTicket


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class MovieTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieTicket
        fields = ("id", "movie", "user", "created", "updated")
        validators = [
            UniqueTogetherValidator(
                queryset=MovieTicket.objects.all(), fields=["movie", "user"]
            )
        ]

    def validate_movie(self, value):
        if MovieTicket.objects.filter(movie=value).count() >= value.number_of_tickets:
            raise serializers.ValidationError(
                _("All the tickets have been sold already!")
            )
        return value
