from django.urls import path
from apps.cart.presentation.api.views import (
    CartView,
    CartAddProductView,
    CartRemoveProductView,
    CartTotalView,
    CartValidateView,
)

urlpatterns = [
    # GET (detalle) y DELETE (vaciar) unificados en CartView para evitar
    # el conflicto de dos path('') apuntando a views distintas.
    path("",              CartView.as_view(),             name="cart"),
    path("items/",        CartAddProductView.as_view(),    name="cart-add-product"),
    path("items/remove/", CartRemoveProductView.as_view(), name="cart-remove-product"),
    path("total/",        CartTotalView.as_view(),         name="cart-total"),
    path("validate/",     CartValidateView.as_view(),      name="cart-validate"),
]
