from djet import assertions
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from users.models import User


class UserAPITestCase(
    APITestCase,
    assertions.StatusCodeAssertionsMixin,
    assertions.EmailAssertionsMixin,
    assertions.InstanceAssertionsMixin,
):
    def setUp(self) -> None:
        self.users_url = reverse("user-list")
        self.login_url = reverse("jwt-create")
        self.me_url = reverse("user-me")
        self.user_data = {
            "first_name": "John",
            "last_name": "Chaplin",
            "email": "john@beatles.com",
            "password": "secret_pass",
            "re_password": "secret_pass",
        }
        self._api_client = APIClient()

    def test_register_user_with_email_success(self):

        response = self._api_client.post(self.users_url, self.user_data)

        self.assert_status_equal(response, status.HTTP_201_CREATED)
        self.assert_instance_exists(User, email=self.user_data["email"])
        self.assert_emails_in_mailbox(1)
        self.assert_email_exists(to=[self.user_data["email"]])

        user = User.objects.get(email=self.user_data["email"])
        self.assertFalse(user.is_active)

    def test_login_success(self):
        user = self._create_user()
        data = {"email": user.email, "password": user.raw_password}
        response = self._api_client.post(self.login_url, data)
        self.assert_status_equal(response, status.HTTP_200_OK)

    def test_get_me_success(self):
        user = self._create_user()
        data = {"email": user.email, "password": user.raw_password}
        response = self._api_client.post(self.login_url, data)

        self._api_client.credentials(
            HTTP_AUTHORIZATION="JWT " + response.data["access"]
        )
        response_me = self._api_client.get(self.me_url)
        self.assert_status_equal(response_me, status.HTTP_200_OK)

    def _create_user(self):
        self.user_data.pop("re_password", None)
        user = User.objects.create_user(**self.user_data)
        user.raw_password = self.user_data["password"]
        return user
