from tempfile import NamedTemporaryFile

from django.db import models
from django.db.models.fields import files

from django.test import Client, TestCase
from django.urls import reverse_lazy

from accounts import models as auth_models
from . import models
# Create your tests here.

class TestJudge(TestCase):

    def setUp(self):
        self.client = Client()
        new_user = auth_models.CustomUser(email="test@test.com", username="test_user")
        new_user.set_password("Buggy@123!!")
        new_user.save()
        self.client.login(**{
            "username": "test_user",
            "password": "Buggy@123!!"
        })
    
    def test_submission(self):

        sample_code = b"print(0)\nprint(1)\nprint(2)\nprint(3)"

        f = NamedTemporaryFile(mode="wb")
        f.write(sample_code)
        f.flush()

        res = self.client.post(reverse_lazy("submit"), data={"seed": 0, "code_file": open(f.name, "rb")})

        first_submission = models.Submission.objects.first()

        self.assertEqual(first_submission.code_file.read(), open(f.name, "rb").read())
        self.assertNotEqual(first_submission.moves_history, "", "No moves were made by submission")
        self.assertNotEqual(first_submission.score, 0, "Score was not recorded for submission")
