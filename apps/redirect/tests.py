from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.url_management.models import RedirectRule


class PublicRedirectTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = get_user_model().objects.create_user(username="user1", password="password1")

        cls.public_redirect = RedirectRule.objects.create(
            owner=cls.user1, redirect_url="https://example.com", is_private=False, redirect_identifier="public123"
        )

    def test_public_redirect(self):
        """Tests accessing a public redirect without authentication"""
        response = self.client.get(reverse("public-redirect", args=[self.public_redirect.redirect_identifier]),
                                   follow=False)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Should redirect
        self.assertEqual(response.url, "https://example.com")

    def test_public_redirect_non_existent(self):
        """Tests that accessing a non-existent public redirect returns 404"""
        response = self.client.get(reverse("public-redirect", args=["nonexistent"]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PrivateRedirectTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = get_user_model().objects.create_user(username="user1", password="password1")
        cls.user2 = get_user_model().objects.create_user(username="user2", password="password2")

        cls.private_redirect = RedirectRule.objects.create(
            owner=cls.user1, redirect_url="https://my-private-cabinet.com", is_private=True,
            redirect_identifier="private123"
        )

        cls.other_users_private_redirect = RedirectRule.objects.create(
            owner=cls.user2, redirect_url="https://other-private-cabinet.com", is_private=True,
            redirect_identifier="forbidden123"
        )

    def setUp(self):
        self.client = APIClient()

    def authenticate_as_user1(self):
        self.client.force_authenticate(user=self.user1)

    def authenticate_as_user2(self):
        self.client.force_authenticate(user=self.user2)

    def test_private_redirect_authenticated_owner(self):
        """Tests accessing a private redirect as the owner"""
        self.authenticate_as_user1()

        response = self.client.get(reverse("private-redirect", args=[self.private_redirect.redirect_identifier]),
                                   follow=False)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Should redirect
        self.assertEqual(response.url, "https://my-private-cabinet.com")

    def test_private_redirect_unauthenticated(self):
        """Tests that an unauthenticated user cannot access a private redirect"""
        response = self.client.get(reverse("private-redirect", args=[self.private_redirect.redirect_identifier]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_private_redirect_other_user(self):
        """Tests that another user cannot access a private redirect (should return 404)"""
        self.authenticate_as_user2()
        response = self.client.get(reverse("private-redirect", args=[self.private_redirect.redirect_identifier]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_private_redirect_non_existent(self):
        """Tests that accessing a non-existent private redirect returns 404"""
        self.authenticate_as_user1()
        response = self.client.get(reverse("private-redirect", args=["nonexistent"]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
