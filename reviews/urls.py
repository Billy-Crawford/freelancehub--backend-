# reviews/urls.py
from django.urls import path
from .views import CreateReviewView

urlpatterns = [
    path("missions/<int:mission_id>/review/", CreateReviewView.as_view()),
]

