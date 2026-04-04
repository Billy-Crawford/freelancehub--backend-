from django.urls import path
from .views import MissionListCreateView, MissionDetailView, ApplyMissionView, UpdateApplicationStatusView, \
    mission_pdf_view

urlpatterns = [
    path('', MissionListCreateView.as_view(), name='missions-list'),
    path('<int:pk>/', MissionDetailView.as_view(), name='mission-detail'),

    path("<int:mission_id>/apply/", ApplyMissionView.as_view(), name="apply-mission"),
    path("<int:mission_id>/applications/<int:pk>/status/", UpdateApplicationStatusView.as_view(), name="update-application-status"),
    path("<int:mission_id>/pdf/", mission_pdf_view, name="mission-pdf"),
]

