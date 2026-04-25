# missions/urls.py
from django.urls import path
from .views import (
    MissionListCreateView,
    MissionDetailView,
    ApplyMissionView,
    UpdateApplicationStatusView,
    MissionApplicationsListView,  # 🔹 import de la nouvelle view
    mission_pdf_view, MyApplicationsView, ClientAcceptedApplicationsView, DeleteMissionView, CompletedMissionListView,
    MissionCanReviewView,
)

urlpatterns = [
    # 🔹 Missions
    path('', MissionListCreateView.as_view(), name='missions-list'),
    path('<int:pk>/', MissionDetailView.as_view(), name='mission-detail'),
    path("my-missions-applications/", ClientAcceptedApplicationsView.as_view()),

    # 🔹 Postuler à une mission (freelance)
    path("<int:mission_id>/apply/", ApplyMissionView.as_view(), name="apply-mission"),
    path("my-applications/", MyApplicationsView.as_view(), name="my-applications"),

    # 🔹 Mettre à jour le statut d'une candidature (client)
    path("<int:mission_id>/applications/<int:pk>/status/", UpdateApplicationStatusView.as_view(), name="update-application-status"),

    # 🔹 Lister toutes les candidatures d'une mission (client)
    path("<int:mission_id>/applications/", MissionApplicationsListView.as_view(), name="mission-applications-list"),

    # 🔹 Générer PDF d'une mission
    path("<int:mission_id>/pdf/", mission_pdf_view, name="mission-pdf"),

    # 🔹 Supprimer une mission
    path("<int:mission_id>/delete/", DeleteMissionView.as_view(), name="delete-mission"),

    # 🔹 regrouper les mission terminees
    path("completed/", CompletedMissionListView.as_view(), name="completed-missions"),

    # 🔹 regrouper les mission terminees
    path("missions/<int:mission_id>/can-review/", MissionCanReviewView.as_view()),
]


