import logging
from django.db.models import Count, Sum
from django.utils.translation import gettext_lazy as _

from apps.orders.infrastructure.factories.notifier_factory import NotifierFactory
from apps.orders.infrastructure.models.order_model import Order
from config.celery import app

logger = logging.getLogger(__name__)


EVENT_TO_HANDLER = {
    "CREATED": "send_order_confirmation",
    "CONFIRMED": "send_order_confirmed",
    "CANCELLED": "send_order_cancelled",
}


@app.task(bind=True, max_retries=3)
def send_order_notification(self, order_id: int, event: str):
    try:
        order = Order.objects.select_related("user").get(pk=order_id)
        handler_name = EVENT_TO_HANDLER.get(event.upper())
        if handler_name is None:
            logger.error(
                "[CELERY] %s",
                _("Evento de pedido no soportado: %(event)s")
                % {"event": event},
            )
            return

        notifier = NotifierFactory.create()
        getattr(notifier, handler_name)(order_id)

        logger.info(
            "[CELERY] %s",
            _(
                "Notificación %(event)s procesada para pedido %(order_id)s"
                " (usuario=%(email)s, estado=%(status)s, entrega=%(delivery)s, total=%(total)s)."
            )
            % {
                "event": event.upper(),
                "order_id": order_id,
                "email": order.user.email,
                "status": order.status,
                "delivery": order.delivery_date.isoformat() if order.delivery_date else _("sin fecha"),
                "total": order.total,
            },
        )
    except Order.DoesNotExist:
        logger.warning(
            "[CELERY] %s",
            _("No se encontró el pedido %(order_id)s para el evento %(event)s.")
            % {"order_id": order_id, "event": event},
        )
    except Exception as exc:
        raise self.retry(exc=exc, countdown=5)


@app.task(bind=True, max_retries=3)
def build_daily_order_report(self, delivery_date: str):
    try:
        orders = Order.objects.filter(delivery_date=delivery_date)
        aggregates = orders.aggregate(
            total_orders=Count("id"),
            total_sales=Sum("total"),
        )
        status_breakdown = {
            row["status"]: row["count"]
            for row in orders.values("status").annotate(count=Count("id"))
        }
        report = {
            "delivery_date": delivery_date,
            "total_orders": aggregates["total_orders"] or 0,
            "total_sales": float(aggregates["total_sales"] or 0),
            "status_breakdown": status_breakdown,
        }
        logger.info(
            "[CELERY] %s",
            _("Reporte diario actualizado para %(delivery_date)s: %(report)s")
            % {"delivery_date": delivery_date, "report": report},
        )
        return report
    except Exception as exc:
        raise self.retry(exc=exc, countdown=5)
