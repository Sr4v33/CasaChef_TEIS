class CartDomainError(Exception):
    pass


class CartIsEmptyError(CartDomainError):
    pass


class ProductAlreadyInCartError(CartDomainError):
    pass


class ProductNotInCartError(CartDomainError):
    pass


class InvalidCartItemData(CartDomainError):
    pass