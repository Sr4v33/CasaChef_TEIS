import os

from apps.payments.domain.ports.payment_processor_port import PaymentProcessorPort
from apps.payments.infrastructure.gateways.mock_payment_processor import MockPaymentProcessor
from apps.payments.infrastructure.gateways.bank_payment_processor import BankPaymentProcessor


class PaymentFactory:
    """Factory Method para seleccionar el procesador de pago por configuración.

    La idea es mover el `if/else` de creación a una fábrica, para que
    la capa de presentación no se entere de detalles técnicos, y el cambio sea por
    configuración (p.ej. env var PAYMENT_PROVIDER).
    """

    @staticmethod
    def create() -> PaymentProcessorPort:
        provider = os.getenv("PAYMENT_PROVIDER", "MOCK").upper()

        if provider == "BANK":
            return BankPaymentProcessor()

        # Si luego agregas PayPal/Stripe, lo agregas aquí sin tocar la vista (OCP).
        return MockPaymentProcessor()
