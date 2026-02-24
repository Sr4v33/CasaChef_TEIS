# apps/orders/views.py
import json
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.orders.application.services.order_service import OrderService

class CreateOrderView(LoginRequiredMixin, View):

    def post(self, request):
        payload = json.loads(request.body)

        service = OrderService()
        # apps/orders/views.py
        try:
            order_id = service.create_order(user=request.user, data=payload)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)

        return JsonResponse(
            {"order_id": order_id},
            status=201
        )
