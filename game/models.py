from django.db import models
from accounts import models as account_models

# Create your models here.

class Submission(models.Model):

    user = models.ForeignKey(account_models.CustomUser, on_delete=models.CASCADE, null=True)
    code_file = models.FileField(upload_to='code_files/', blank=False, null=False)
    seed = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    moves_history = models.TextField()
    indexes_state = models.TextField()
    status = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True, editable=False)
    is_run = models.BooleanField(default=False)
    errors = models.TextField()