# users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, MeView,
    FreelanceProfileView, ClientProfileView,
    PublicFreelanceProfileView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeView.as_view(), name='me'),
    path('profile/freelance/', FreelanceProfileView.as_view(), name='freelance-profile'),
    path('profile/client/', ClientProfileView.as_view(), name='client-profile'),
    path('freelances/<int:pk>/', PublicFreelanceProfileView.as_view(), name='public-freelance'),
]

