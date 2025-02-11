from django.test import TestCase
from django.contrib.auth.models import Permission
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()


class UserRegistrationAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(role='admin', email='me@sample.com', password='1234')
        self.register_url = reverse("register")

    def test_create_super_user(self):
        data = {
            "role": "admin", "email": "me2@sample.com", "password": "1234"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)  # One existing + one new blog
        self.assertEqual(response.data["role"], "admin")
        print('create user test case passed')
