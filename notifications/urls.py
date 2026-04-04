from django.urls import path
from .views import NotificationListView, MarkAsReadView, UnreadCountView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications'),
    path("<int:pk>/read/", MarkAsReadView.as_view(), name='mark_as_read'),
    path("unread-count/", UnreadCountView.as_view(), name='unread-count'),
]

