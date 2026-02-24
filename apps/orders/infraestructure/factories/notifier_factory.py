import os
from abc import ABC, abstractmethod


class Notifier(ABC):

    @abstractmethod
    def send_order_confirmation(self, order_id: int):
        pass


class ConsoleNotifier(Notifier):

    def send_order_confirmation(self, order_id: int):
        print(f"[DEV] Pedido {order_id} confirmado")


class EmailNotifier(Notifier):

    def send_order_confirmation(self, order_id: int):
        # integración real iría aquí
        print(f"[PROD] Email enviado para el pedido {order_id}")


class NotifierFactory:

    @staticmethod
    def create() -> Notifier:
        env = os.getenv("ENV_TYPE", "DEV")

        if env == "PROD":
            return EmailNotifier()

        return ConsoleNotifier()
