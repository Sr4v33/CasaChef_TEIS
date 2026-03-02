from django.urls import path
from apps.dishes.presentation.api.views import (
    ProductRegisterView,
    ProductDetailView,
)

urlpatterns = [
    path("",                     ProductRegisterView.as_view(), name="product-register"),
    path("<uuid:product_id>/",   ProductDetailView.as_view(),   name="product-detail"),
]