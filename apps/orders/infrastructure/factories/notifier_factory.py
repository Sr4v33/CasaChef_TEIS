import os
import logging
from abc import ABC, abstractmethod
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class Notifier(ABC):

    @abstractmethod
    def send_order_confirmation(self, order_id: int) -> None:
        pass

    @abstractmethod
    def send_order_confirmed(self, order_id: int) -> None:
        pass

    @abstractmethod
    def send_order_cancelled(self, order_id: int) -> None:
        pass


class ConsoleNotifier(Notifier):

    def send_order_confirmation(self, order_id: int) -> None:
        logger.info(
            "[DEV] %s",
            _("Pedido %(order_id)s recibido. Confirmación enviada.")
            % {"order_id": order_id},
        )

    def send_order_confirmed(self, order_id: int) -> None:
        logger.info(
            "[DEV] %s",
            _("Pedido %(order_id)s confirmado.") % {"order_id": order_id},
        )

    def send_order_cancelled(self, order_id: int) -> None:
        logger.info(
            "[DEV] %s",
            _("Pedido %(order_id)s cancelado.") % {"order_id": order_id},
        )


class EmailNotifier(Notifier):

    def send_order_confirmation(self, order_id: int) -> None:
        logger.info(
            "[EMAIL] %s",
            _("Correo de confirmación enviado para el pedido %(order_id)s.")
            % {"order_id": order_id},
        )

    def send_order_confirmed(self, order_id: int) -> None:
        logger.info(
            "[EMAIL] %s",
            _("Correo de pedido confirmado enviado para %(order_id)s.")
            % {"order_id": order_id},
        )

    def send_order_cancelled(self, order_id: int) -> None:
        logger.info(
            "[EMAIL] %s",
            _("Correo de pedido cancelado enviado para %(order_id)s.")
            % {"order_id": order_id},
        )


class NotifierFactory:

    @staticmethod
    def create() -> Notifier:
        notifier_name = os.getenv("NOTIFIER", "").strip().upper()
        if notifier_name == "EMAIL":
            return EmailNotifier()
        if notifier_name == "CONSOLE":
            return ConsoleNotifier()

        env = os.getenv("ENV_TYPE", "DEV").strip().upper()
        if env == "PROD":
            return EmailNotifier()
        return ConsoleNotifier()
