from djet import assertions
from model_bakery import baker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from movies.models import Movie
from users.models import User


class MovieAPITestCase(
    APITestCase,
    assertions.StatusCodeAssertionsMixin,
    assertions.EmailAssertionsMixin,
    assertions.InstanceAssertionsMixin,
):
    def setUp(self) -> None:
        self._movies_list_url = reverse("movies:movie-list")
        self._user = baker.make(User)
        self._client = APIClient()
        self._client.force_authenticate(self._user)

    def test_list_paginated_movies_success(self):
        baker.make(Movie, _quantity=30)
        response = self._client.get(self._movies_list_url)
        self.assert_status_equal(response, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 20)

    def test_get_single_movie_with_slug(self):
        movie = baker.make(Movie, name="Lord of the Ring")
        movie_detail_url = reverse("movies:movie-detail", kwargs={"slug": movie.slug})
        response = self._client.get(movie_detail_url)
        self.assert_status_equal(response, status.HTTP_200_OK)
        self.assertEqual(response.data["slug"], movie.slug)
