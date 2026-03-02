from typing import Optional
from uuid import UUID

from apps.users.domain.entities.user import User
from apps.users.domain.ports.user_repository_port import UserRepositoryPort
from apps.users.infrastructure.models.user_model import UserModel


class DjangoUserRepository(UserRepositoryPort):
    """Implementación del puerto UserRepositoryPort usando el ORM de Django.

    Mantiene el ORM confinado en la capa de infraestructura: el dominio y
    la capa de aplicación nunca importan modelos Django directamente.
    """

    def save(self, user: User) -> User:
        UserModel.objects.update_or_create(
            id=user.id,
            defaults={
                "email": user.email,
                "active": user.active,
            },
        )
        return user

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        try:
            m = UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            return None
        return User(email=m.email, active=m.active, user_id=m.id)

    def get_by_email(self, email: str) -> Optional[User]:
        try:
            m = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        return User(email=m.email, active=m.active, user_id=m.id)

    def exists_by_email(self, email: str) -> bool:
        return UserModel.objects.filter(email=email).exists()

    def delete(self, user_id: UUID) -> None:
        UserModel.objects.filter(id=user_id).delete()