from model_bakery import baker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from movies.models import Movie, MovieTicket
from users.models import User


class MovieTicketAPITestCase(APITestCase):
    def setUp(self) -> None:
        self._movie_ticket_list_url = reverse("movies:movieticket-list")
        self._user = baker.make(User)
        self._client = APIClient()
        self._client.force_authenticate(self._user)

    def test_purchase_ticket_successful(self):
        movie = baker.make(Movie)
        data = {"movie": movie.id}
        response = self._client.post(self._movie_ticket_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_one_user_can_purchase_only_one_ticket_of_a_movie(self):
        movie = baker.make(Movie)
        baker.make(MovieTicket, movie=movie, user=self._user)
        data = {"movie": movie.id}
        response = self._client.post(self._movie_ticket_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_all_tickets_of_a_movie_purchased_already(self):
        movie = baker.make(Movie, number_of_tickets=1)
        baker.make(MovieTicket, movie=movie, user=self._user)

        self._client.force_authenticate(baker.make(User))
        data = {"movie": movie.id}
        response = self._client.post(self._movie_ticket_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_list_of_purchased_tickets(self):
        movie_1 = baker.make(Movie)
        movie_2 = baker.make(Movie)
        baker.make(MovieTicket, movie=movie_1, user=self._user)
        baker.make(MovieTicket, movie=movie_2, user=self._user)

        response = self._client.get(self._movie_ticket_list_url)
        self.assertCountEqual(
            [str(movie_1.id), str(movie_2.id)],
            [movie_ticket["movie"]["id"] for movie_ticket in response.data["results"]],
        )

    def test_non_owner_cant_get_others_list_of_tickets(self):
        baker.make(MovieTicket, movie=baker.make(Movie), user=self._user)
        baker.make(MovieTicket, movie=baker.make(Movie), user=self._user)

        self._client.force_authenticate(baker.make(User))
        response = self._client.get(self._movie_ticket_list_url)
        self.assertEqual(len([each["movie"] for each in response.data["results"]]), 0)

    def test_get_a_purchased_ticket(self):
        movie_ticket = baker.make(MovieTicket, movie=baker.make(Movie), user=self._user)
        movie_detail_url = reverse(
            "movies:movieticket-detail", kwargs={"pk": movie_ticket.id}
        )
        response = self._client.get(movie_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_owner_cant_get_others_single_ticket(self):
        baker.make(MovieTicket, movie=baker.make(Movie), user=self._user)
        movie_ticket = baker.make(MovieTicket, movie=baker.make(Movie), user=self._user)

        self._client.force_authenticate(baker.make(User))
        movie_detail_url = reverse(
            "movies:movieticket-detail", kwargs={"pk": movie_ticket.id}
        )
        response = self._client.get(movie_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
