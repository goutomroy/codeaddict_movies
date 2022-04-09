from model_bakery import baker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from movies.models import Movie, MovieTicket
from users.models import User


class MovieTicketAPITestCase(APITestCase):
    def setUp(self) -> None:
        self._movies_list_url = reverse("movies:movieticket-list")
        self._user = baker.make(User)
        self._client = APIClient()
        self._client.force_authenticate(self._user)

    def test_purchase_ticket_successful(self):
        movie = baker.make(Movie)
        data = {"movie": movie.id, "user": self._user.id}
        response = self._client.post(self._movies_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_one_user_can_purchase_only_one_ticket_of_a_movie(self):
        movie = baker.make(Movie)
        baker.make(MovieTicket, movie=movie, user=self._user)
        data = {"movie": movie.id, "user": self._user.id}
        response = self._client.post(self._movies_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_all_tickets_of_a_movie_purchased_already(self):
        movie = baker.make(Movie, number_of_tickets=1)
        baker.make(MovieTicket, movie=movie, user=self._user)

        another_user = baker.make(User)
        self._client.force_authenticate(another_user)
        data = {"movie": movie.id, "user": another_user.id}
        response = self._client.post(self._movies_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_list_of_purchased_tickets(self):
        movie_1 = baker.make(Movie)
        movie_2 = baker.make(Movie)
        baker.make(MovieTicket, movie=movie_1, user=self._user)
        baker.make(MovieTicket, movie=movie_2, user=self._user)

        response = self._client.get(self._movies_list_url)
        self.assertCountEqual(
            [movie_1.id, movie_2.id],
            [each["movie"] for each in response.data["results"]],
        )

    def test_get_a_purchased_ticket(self):
        movie_ticket = baker.make(MovieTicket, movie=baker.make(Movie), user=self._user)
        movie_detail_url = reverse(
            "movies:movieticket-detail", kwargs={"pk": movie_ticket.id}
        )
        response = self._client.get(movie_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
