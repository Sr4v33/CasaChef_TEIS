class DishesDomainError(Exception):
    """Errores de dominio para el contexto de Platos/Productos."""
    pass


class InvalidProductData(DishesDomainError):
    pass


class InsufficientStock(DishesDomainError):
    pass
