from django.urls import path
from .views import (
    CreatePaymentView,
    ReleasePaymentView,
    CancelPaymentView,
    MyPaymentsView
)

urlpatterns = [
    path("my/", MyPaymentsView.as_view()),
    path("<int:mission_id>/pay/", CreatePaymentView.as_view()),
    path("<int:mission_id>/cancel/", CancelPaymentView.as_view()),
    path("<int:mission_id>/release/", ReleasePaymentView.as_view()),
]

