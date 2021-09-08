from django.shortcuts import render
from django.views import generic
from django.contrib.auth import mixins
from django.urls import reverse_lazy

from . import models, forms, judge

# Create your views here.

class SubmitCodeView(mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Submission
    # form_class = forms.SubmissionForm
    fields = ['code_file', 'seed']
    success_url = reverse_lazy("history")
    
    def form_valid(self, form):
        ret = super().form_valid(form)
        self.object.user = self.request.user
        self.object.save()
        judge_obj = judge.Judge(self.object)
        judge_obj.start()
        return ret

class ListHistory(mixins.LoginRequiredMixin, generic.ListView):
    model = models.Submission
    ordering = ('-score',)

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(user=self.request.user)

class Leaderboard(generic.ListView):
    model = models.Submission
    ordering = ('-score',)
    template_name = "game/leaderboard.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs).filter(seed=0)
        # TODO: Filter out same score submission by same person
        return qs[:50]

class SubmissionDetail(generic.DetailView):
    model = models.Submission
    
    def get_context_data(self, **kwargs):
        kwargs.update({
            "moves": [int(i) for i in list(self.object.moves_history)]
        })
        return super().get_context_data(**kwargs)

class RejudeAll(generic.TemplateView):
    template_name = "game/leaderboard.html"

    def get(self, *args, **kwargs):
        qs = models.Submission.objects.all()
        for subm in qs:
            judge_obj = judge.Judge(subm)
            judge_obj.start()
            judge_obj.join()
        return super().get(*args, **kwargs)