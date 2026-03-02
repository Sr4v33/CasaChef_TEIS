from django.urls import path
from apps.payments.presentation.api.views import (
    PayOrderView,
    PaymentDetailView,
)

urlpatterns = [
    path("",                     PayOrderView.as_view(),     name="payment-pay"),
    path("<uuid:payment_id>/",   PaymentDetailView.as_view(), name="payment-detail"),
]