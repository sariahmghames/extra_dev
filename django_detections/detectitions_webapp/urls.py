from django.urls import path

from . import views


app_name = "polls_app" # app namespace
urlpatterns = [
    path('react/', views.react_app_view, name='react_app_view'),
    path('api/detect/', views.DetectionAPIView.as_view(), name='detection_api'),
    # ex: /polls/ is the URL to use to access the view
    path("", views.index, name="index"),
    # ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),

]