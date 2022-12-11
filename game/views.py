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
        judge.judge(self.object)
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
        ret = set()
        for s in qs:
            if s.score not in ret:
                ret.add(s.score)
                yield s
            if len(ret) >= 50:
                break

class SubmissionDetail(generic.DetailView):
    model = models.Submission
    
    def get_context_data(self, **kwargs):
        print(self.object.indexes_state)
        kwargs.update({
            "is_processing": eval(self.object.indexes_state)==[],
            "moves": [int(i) for i in list(self.object.moves_history.split(",")) if i],
            "indexes": [[i[0]*4 + i[1], j] for i,j in eval(self.object.indexes_state.replace("'",""))]
        })
        return super().get_context_data(**kwargs)
