# reviews/urls.py
from django.urls import path
from .views import CreateReviewView, UserReviewsView

urlpatterns = [
    path("missions/<int:mission_id>/review/", CreateReviewView.as_view()),
    path("users/<int:user_id>/reviews/", UserReviewsView.as_view()),
]

