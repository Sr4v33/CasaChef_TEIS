class PaymentsDomainError(Exception):
    """Errores de dominio para pagos."""
    pass


class InvalidPaymentData(PaymentsDomainError):
    pass


class InvalidPaymentTransition(PaymentsDomainError):
    pass


class PaymentProcessingError(PaymentsDomainError):
    pass
