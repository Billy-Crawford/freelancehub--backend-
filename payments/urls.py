from django.urls import path
from .views import CreatePaymentView

urlpatterns = [
    path("missions/<int:mission_id>/pay/", CreatePaymentView.as_view()),
]

