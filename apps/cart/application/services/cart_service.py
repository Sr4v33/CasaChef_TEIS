from decimal import Decimal
from uuid import UUID

from apps.cart.domain.entities.cart import CartEntity
from apps.cart.domain.exceptions import CartIsEmptyError, ProductNotInCartError
from apps.cart.domain.ports.cart_repository_port import CartRepositoryPort
from apps.cart.domain.ports.stock_checker_port import StockCheckerPort


class CartService:
    """Service Layer para casos de uso del Carrito.

    Orquesta los flujos sin contener lógica de negocio (que vive en la entidad Cart).
    Cumple SRP: cada método corresponde a un caso de uso concreto.

    Inyección de dependencias via constructor (facilita tests con mocks).
    """

    def __init__(
        self,
        cart_repo: CartRepositoryPort,
        stock_checker: StockCheckerPort,
    ) -> None:
        self._cart_repo = cart_repo
        self._stock_checker = stock_checker

    # --------------------------------------------------
    # Casos de uso
    # --------------------------------------------------

    def get_or_create_cart(self, customer_id: UUID) -> CartEntity:
        """Retorna el carrito activo del cliente, o crea uno nuevo."""
        cart = self._cart_repo.get_by_customer_id(customer_id)
        if cart is None:
            cart = CartEntity(customer_id=customer_id)
            cart = self._cart_repo.save(cart)
        return cart

    def add_product(
        self,
        *,
        customer_id: UUID,
        product_id: UUID,
        quantity: int,
        unit_price: Decimal,
    ) -> CartEntity:
        """Añade (o acumula) un producto en el carrito del cliente."""
        cart = self.get_or_create_cart(customer_id)
        cart.add_product(
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
        )
        return self._cart_repo.save(cart)

    def remove_product(
        self,
        *,
        customer_id: UUID,
        product_id: UUID,
    ) -> CartEntity:
        """Elimina un producto del carrito."""
        cart = self._get_existing_cart(customer_id)
        cart.remove_product(product_id)
        return self._cart_repo.save(cart)

    def calculate_total(self, *, customer_id: UUID) -> Decimal:
        """Retorna el total actual del carrito sin persistir nada."""
        cart = self._get_existing_cart(customer_id)
        return cart.calculate_total()

    def validate_availability(self, *, customer_id: UUID) -> None:
        """Valida que todos los productos del carrito tengan stock.

        Delega en StockCheckerPort para no acoplar el dominio a infraestructura.
        Lanza excepción si algún producto no tiene stock suficiente.
        """
        cart = self._get_existing_cart(customer_id)
        cart.validate_availability(self._stock_checker)

    def clear_cart(self, *, customer_id: UUID) -> None:
        """Vacía y elimina el carrito (se llama tras convertir a Order)."""
        cart = self._cart_repo.get_by_customer_id(customer_id)
        if cart:
            self._cart_repo.delete(cart.cart_id)

    def get_cart(self, *, customer_id: UUID) -> CartEntity:
        """Retorna el carrito del cliente (crea uno vacío si no existe)."""
        return self.get_or_create_cart(customer_id)

    # --------------------------------------------------
    # Helpers privados
    # --------------------------------------------------

    def _get_existing_cart(self, customer_id: UUID) -> CartEntity:
        cart = self._cart_repo.get_by_customer_id(customer_id)
        if cart is None:
            raise CartIsEmptyError("El cliente no tiene un carrito activo")
        return cart