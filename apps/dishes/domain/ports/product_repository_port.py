from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from ..entities.product import ProductEntity

class ProductRepositoryPort(ABC):
    @abstractmethod
    def save(self, product: ProductEntity) -> ProductEntity:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, product_id: UUID) -> Optional[ProductEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[ProductEntity]:
        raise NotImplementedError