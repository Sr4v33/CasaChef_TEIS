from uuid import UUID

from apps.cart.domain.exceptions import CartDomainError
from apps.cart.domain.ports.stock_checker_port import StockCheckerPort
from apps.dishes.infrastructure.models.product_model import ProductModel


class ProductStockChecker(StockCheckerPort):
    """Implementación concreta de StockCheckerPort.

    Consulta ProductModel para verificar disponibilidad.
    Vive en infraestructura para mantener el dominio libre de dependencias ORM.
    """

    def check(self, product_id: UUID, quantity: int) -> None:
        try:
            product = ProductModel.objects.get(id=product_id, active=True)
        except ProductModel.DoesNotExist:
            raise CartDomainError(
                f"El producto {product_id} no existe o no está disponible"
            )

        if product.stock < quantity:
            raise CartDomainError(
                f"Stock insuficiente para '{product.name}'. "
                f"Disponible={product.stock}, solicitado={quantity}"
            )