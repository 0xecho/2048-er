from django import forms

class SubmissionForm(forms.Form):

    # user = models.ForeignKey(account_models.CustomUser, on_delete=models.CASCADE)
    code_file = forms.FileField(allow_empty_file=False, required=True)
    seed = forms.IntegerField()
    score = forms.IntegerField()