from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from . import models

# Create your tests here.
User = get_user_model()


class SignUpTest(TestCase):

    def setUp(self) -> None:
        self.credentials = {
            "first_name": "Test",
            "last_name": "User1",
            "username": "test_user1",
            "email": "testuser@testuser.com",
            "password1": "Buggy@123!!",
            "password2": "Buggy@123!!",
        }
        self.client = Client()

    def test_signup(self):
        res = self.client.post("/accounts/signup/", self.credentials)
        new_user = User.objects.filter(
            username=self.credentials.get("username")).first()

        self.assertIsNotNone(new_user)


class LoginTest(TestCase):

    def setUp(self) -> None:
        self.credentials = {
            "first_name": "Test",
            "last_name": "User1",
            "username": "test_user1",
            "email": "testuser@testuser.com",
            "password": "Buggy@123!!",
        }
        self.client = Client()
        user = User.objects.create(**self.credentials)
        user.set_password(self.credentials.get("password"))
        user.save()
        self.credentials.update({"login": "testuser@testuser.com", })

    def test_login(self):
        res = self.client.post("/accounts/login/", self.credentials)
        res = self.client.get("/history/")
        self.assertEqual(res.status_code, 200)
