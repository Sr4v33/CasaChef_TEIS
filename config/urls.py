"""URL configuration for CasaChef project.

API Gateway central — todos los módulos se montan bajo /api/.
Estructura:
    /api/products/    → apps.dishes
    /api/orders/      → apps.orders
    /api/payments/    → apps.payments
    /api/users/       → apps.users
    /api/cart/        → apps.cart
    /api/production/  → apps.production
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_root(request):
    base = request.build_absolute_uri('/api/')
    return Response({
        'register':       base + 'users/register/',
        'login':          base + 'auth/login/',
        'addresses':      base + 'users/me/addresses/',
        'products':       base + 'products/',
        'orders':         base + 'orders/',
        'payments':       base + 'payments/',
        'cart':           base + 'cart/',
        'production':     base + 'production/',
    })

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/",          api_root),
    # path("", api_root),
    path("", TemplateView.as_view(template_name="index.html")),
    path("api/products/", include("apps.dishes.presentation.api.urls")),
    path("api/orders/",   include("apps.orders.presentation.api.urls")),
    path("api/users/",    include("apps.users.presentation.api.urls")),
    path("api/payments/", include("apps.payments.presentation.api.urls")),
    path("api/cart/",     include("apps.cart.presentation.api.urls")),
    path("api/production/", include("apps.production.presentation.api.urls")),
    path("api/auth/",     include("rest_framework.urls")),
]