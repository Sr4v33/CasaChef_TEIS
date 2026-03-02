from django.urls import path
from apps.cart.presentation.api.views import (
    CartDetailView,
    CartAddProductView,
    CartRemoveProductView,
    CartTotalView,
    CartValidateView,
)

urlpatterns = [
    path("", CartDetailView.as_view(), name="cart-detail"),
    path("items/", CartAddProductView.as_view(), name="cart-add-product"),
    path("items/remove/", CartRemoveProductView.as_view(), name="cart-remove-product"),
    path("total/", CartTotalView.as_view(), name="cart-total"),
    path("validate/", CartValidateView.as_view(), name="cart-validate"),
]