from djet import assertions
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from users.models import User


class UserAPITestCase(
    APITestCase,
    assertions.StatusCodeAssertionsMixin,
    assertions.EmailAssertionsMixin,
    assertions.InstanceAssertionsMixin,
):
    def setUp(self) -> None:
        self._users_url = reverse("user-list")
        self._login_url = reverse("jwt-create")
        self._me_url = reverse("user-me")
        self._user_data = {
            "first_name": "John",
            "last_name": "Chaplin",
            "email": "john@beatles.com",
            "password": "secret_pass",
            "re_password": "secret_pass",
        }

    def test_register_user_with_email_success(self):

        response = self.client.post(self._users_url, self._user_data)

        self.assert_status_equal(response, status.HTTP_201_CREATED)
        self.assert_instance_exists(User, email=self._user_data["email"])
        self.assert_emails_in_mailbox(1)
        self.assert_email_exists(to=[self._user_data["email"]])

        user = User.objects.get(email=self._user_data["email"])
        self.assertFalse(user.is_active)

    def test_login_success(self):
        user = self._create_user()
        data = {"email": user.email, "password": user.raw_password}
        response = self.client.post(self._login_url, data)
        self.assert_status_equal(response, status.HTTP_200_OK)

    def test_get_me_success(self):
        user = self._create_user()
        data = {"email": user.email, "password": user.raw_password}
        response = self.client.post(self._login_url, data)

        self.client.credentials(HTTP_AUTHORIZATION="JWT " + response.data["access"])
        response_me = self.client.get(self._me_url)
        self.assert_status_equal(response_me, status.HTTP_200_OK)

    def _create_user(self):
        self._user_data.pop("re_password", None)
        user = User.objects.create_user(**self._user_data)
        user.raw_password = self._user_data["password"]
        return user
