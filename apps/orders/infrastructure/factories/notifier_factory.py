import os
from abc import ABC, abstractmethod


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
        print(f"[DEV] Pedido {order_id} recibido — confirmación enviada")

    def send_order_confirmed(self, order_id: int) -> None:
        print(f"[DEV] Pedido {order_id} confirmado")

    def send_order_cancelled(self, order_id: int) -> None:
        print(f"[DEV] Pedido {order_id} cancelado")


class EmailNotifier(Notifier):

    def send_order_confirmation(self, order_id: int) -> None:
        print(f"[PROD] Email de confirmación enviado para el pedido {order_id}")

    def send_order_confirmed(self, order_id: int) -> None:
        print(f"[PROD] Email 'pedido confirmado' enviado para {order_id}")

    def send_order_cancelled(self, order_id: int) -> None:
        print(f"[PROD] Email 'pedido cancelado' enviado para {order_id}")


class NotifierFactory:

    @staticmethod
    def create() -> Notifier:
        env = os.getenv("ENV_TYPE", "DEV")
        if env == "PROD":
            return EmailNotifier()
        return ConsoleNotifier()