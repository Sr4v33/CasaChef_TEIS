from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from ..entities.user import User


class UserRepositoryPort(ABC):

    @abstractmethod
    def save(self, user: User) -> User:
        # Guarda el usuario
        pass

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> Optional[User]:
        # Obtiene un usuario por su ID
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        # Obtiene un usuario por su email
        pass

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        # Verifica si un usuario existe por su email
        pass

    @abstractmethod
    def delete(self, user_id: UUID) -> None:
        # Elimina un usuario por su ID
        pass