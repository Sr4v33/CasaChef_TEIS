from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from ..entities.payment import PaymentEntity


class PaymentRepositoryPort(ABC):
    @abstractmethod
    def save(self, payment: PaymentEntity) -> PaymentEntity:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, payment_id: UUID) -> Optional[PaymentEntity]:
        raise NotImplementedError
