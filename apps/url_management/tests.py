from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from apps.url_management.models import RedirectRule


class RedirectRuleViewSetTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username="user1", password="password1")
        cls.user2 = User.objects.create_user(username="user2", password="password2")

        cls.redirect1 = RedirectRule.objects.create(
            owner=cls.user1, redirect_url="https://google.com", is_private=False
        )
        cls.redirect2 = RedirectRule.objects.create(
            owner=cls.user2, redirect_url="https://github.com", is_private=True
        )

    def setUp(self):
        self.client = APIClient()

    def authenticate_as_user1(self):
        self.client.force_authenticate(user=self.user1)

    def authenticate_as_user2(self):
        self.client.force_authenticate(user=self.user2)

    def test_create_redirect(self):
        """Tests creating a new redirect rule"""
        self.authenticate_as_user1()
        data = {"redirect_url": "https://example.com", "is_private": False}
        response = self.client.post(reverse("redirectrule-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RedirectRule.objects.count(), 3)

    def test_list_redirects(self):
        """Tests retrieving the list of redirect rules"""
        self.authenticate_as_user1()
        response = self.client.get(reverse("redirectrule-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # user1 should only see their own redirects

    def test_retrieve_redirect(self):
        """Tests retrieving a specific redirect rule"""
        self.authenticate_as_user1()

        response = self.client.get(reverse("redirectrule-detail", args=[self.redirect1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse("redirectrule-detail", args=[self.redirect2.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_redirect(self):
        """Tests updating own redirect rule"""
        self.authenticate_as_user1()
        data = {"is_private": True}
        response = self.client.patch(reverse("redirectrule-detail", args=[self.redirect1.id]), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.redirect1.refresh_from_db()
        self.assertTrue(self.redirect1.is_private)

    def test_update_other_users_redirect(self):
        """Tests trying to update another user's redirect rule"""
        self.authenticate_as_user1()
        data = {"is_private": False}
        response = self.client.patch(reverse("redirectrule-detail", args=[self.redirect2.id]), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_redirect(self):
        """Tests deleting own redirect rule"""
        self.authenticate_as_user1()
        response = self.client.delete(reverse("redirectrule-detail", args=[self.redirect1.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(RedirectRule.objects.filter(id=self.redirect1.id).exists())

    def test_delete_other_users_redirect(self):
        """Tests trying to delete another user's redirect rule"""
        self.authenticate_as_user1()
        response = self.client.delete(reverse("redirectrule-detail", args=[self.redirect2.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_user_cannot_create_redirect(self):
        """Tests that an unauthenticated user cannot create a redirect rule"""
        self.client.force_authenticate(user=None)
        data = {"redirect_url": "https://example.com", "is_private": False}
        response = self.client.post(reverse("redirectrule-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_access_redirects(self):
        """Tests that an unauthenticated user cannot access any redirect rules (GET, PATCH, DELETE)"""
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("redirectrule-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(reverse("redirectrule-detail", args=[self.redirect1.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.patch(reverse("redirectrule-detail", args=[self.redirect1.id]), {"is_private": True},
                                     format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.delete(reverse("redirectrule-detail", args=[self.redirect1.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
