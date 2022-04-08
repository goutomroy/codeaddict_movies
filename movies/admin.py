from django.contrib import admin

from movies.models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug", "ticket_price", "number_of_tickets", "rating"]
