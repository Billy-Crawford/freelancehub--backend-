# chat/urls.py
from django.urls import path
from .views import ConversationListView, MessageListCreateView

urlpatterns = [
    path("conversations/", ConversationListView.as_view()),
    path("messages/<int:mission_id>/", MessageListCreateView.as_view()),
]

