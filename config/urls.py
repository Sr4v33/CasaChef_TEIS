"""URL configuration for CasaChef project.

API Gateway central — todos los módulos se montan bajo /api/.
Estructura:
    /api/products/   → apps.dishes
    /api/orders/     → apps.orders
    /api/payments/   → apps.payments
    /api/users/      → apps.users
    /api/cart/       → apps.cart
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/products/", include("apps.dishes.presentation.api.urls")),
    path("api/orders/",    include("apps.orders.presentation.api.urls")),
    path("api/users/",   include("apps.users.presentation.api.urls")),
    path("api/payments/",   include("apps.payments.presentation.api.urls")),
    path("api/cart/",   include("apps.cart.presentation.api.urls")),

    path("api/auth/", include("rest_framework.urls")),
]
