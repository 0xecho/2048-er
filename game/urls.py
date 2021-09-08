from django.urls import path

from . import views

urlpatterns = [
    path('submit/', views.SubmitCodeView.as_view(), name='submit'),
    path('history/', views.ListHistory.as_view(), name='history'),
    path('leaderboard/', views.Leaderboard.as_view(), name='leaderboard'),
    path('history/<int:pk>', views.SubmissionDetail.as_view(), name='submission_detail'),
    path('rejudge/all', views.RejudeAll.as_view(), name='submission_detail'),
]
