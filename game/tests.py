from tempfile import NamedTemporaryFile

from django.db import models
from django.db.models.fields import files

from django.test import Client, TestCase
from django.urls import reverse_lazy

from accounts import models as auth_models
from game.judge import judge_worker
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

        sample_code = b"""for i in range(10):
	for _ in range(4):
		x = input()
	print(i%4)"""

        f = NamedTemporaryFile(mode="wb")
        f.write(sample_code)
        f.flush()

        # res = self.client.post(reverse_lazy("submit"), data={"seed": 0, "code_file": open(f.name, "rb")})
        new_submission = models.Submission.objects.create(
            user=auth_models.CustomUser.objects.get(username="test_user"),
            seed=0,
        )
        new_submission.code_file.save("test.py", files.File(open(f.name, 'rb')), save=True)
        new_submission.save()

        first_submission = models.Submission.objects.first()

        self.assertEqual(first_submission.code_file.read(), open(f.name, "rb").read())
    
        judge_worker(first_submission)

        self.assertNotEqual(first_submission.score, 0, "Score was not recorded for submission")
        self.assertNotEqual(first_submission.moves_history, "", "No moves were made by submission")
    
    def test_leaderboards(self):
        res = self.client.get(reverse_lazy("leaderboard"))
        self.assertEqual(res.status_code, 200, "Leaderboards page did not load")
        
