from django.urls import path
from apps.dishes.presentation.api.views import (
    ProductRegisterView,
    ProductDetailView,
    ProductByNameView,
)

urlpatterns = [
    path("",                     ProductRegisterView.as_view(), name="product-register"),
    path("by-name/",             ProductByNameView.as_view(),   name="product-by-name"),
    path("<uuid:product_id>/",   ProductDetailView.as_view(),   name="product-detail"),
]