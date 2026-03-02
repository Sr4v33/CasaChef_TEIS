from django.urls import path
from apps.orders.presentation.api.views import (
    OrderCreateView,
    OrderDetailView,
    OrderConfirmView,
    OrderCancelView,
    OrderValidateStockView,
)

urlpatterns = [
    path("",                                OrderCreateView.as_view(),       name="order-create"),
    path("<int:order_id>/",                 OrderDetailView.as_view(),       name="order-detail"),
    path("<int:order_id>/confirm/",         OrderConfirmView.as_view(),      name="order-confirm"),
    path("<int:order_id>/cancel/",          OrderCancelView.as_view(),       name="order-cancel"),
    path("<int:order_id>/validate-stock/",  OrderValidateStockView.as_view(), name="order-validate-stock"),
]