from django.urls import path
from .views import MissionListCreateView, MissionDetailView

urlpatterns = [
    path('', MissionListCreateView.as_view(), name='missions-list'),
    path('<int:pk>/', MissionDetailView.as_view(), name='mission-detail'),
]

