# apps/orders/views.py
import json
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from orders.services import OrderService


class CreateOrderView(LoginRequiredMixin, View):

    def post(self, request):
        payload = json.loads(request.body)

        service = OrderService()
        order_id = service.create_order(
            user=request.user,
            data=payload
        )

        return JsonResponse(
            {"order_id": order_id},
            status=201
        )
