class OrderDomainError(Exception):
    pass


class OrderNotFoundError(OrderDomainError):
    pass


class InvalidOrderTransition(OrderDomainError):
    pass


class InsufficientProductionStock(OrderDomainError):
    pass