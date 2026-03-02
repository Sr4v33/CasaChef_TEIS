from typing import List, Optional

from apps.users.domain.entities.address import Address
from apps.users.domain.entities.cook import CookProfile
from apps.users.domain.entities.customer import CustomerProfile
from apps.users.domain.entities.user import User
from apps.users.domain.exceptions import UserDomainError
from apps.users.domain.ports.user_repository_port import UserRepositoryPort
from apps.users.infrastructure.models.address_model import AddressModel
from apps.users.infrastructure.models.cook_model import CookModel
from apps.users.infrastructure.models.customer_model import CustomerModel
from apps.users.infrastructure.models.user_model import UserModel


class UserService:
    """Service Layer para gestión de usuarios.

    Orquesta todos los casos de uso relacionados con User, CustomerProfile,
    CookProfile y Address. Ninguna vista debe contener llamadas al ORM directamente.
    Cumple SRP: cada método representa un único caso de uso.
    """

    def __init__(self, repo: UserRepositoryPort) -> None:
        self._repo = repo

    # ──────────────────────────────────────────────
    # Caso de uso: Registro de usuario
    # ──────────────────────────────────────────────

    def register_user(self, email: str, password: str) -> dict:
        """Registra un nuevo usuario en Django Auth y devuelve sus datos básicos.

        Raises:
            UserDomainError: si el email ya está registrado.
            ValueError: si el email no es válido (validado por la entidad User).
        """
        # Validación de dominio antes de tocar infraestructura
        User(email=email)

        from django.contrib.auth import get_user_model
        AuthUser = get_user_model()

        if AuthUser.objects.filter(username=email).exists():
            raise UserDomainError(f"Ya existe un usuario con el email '{email}'.")

        django_user = AuthUser.objects.create_user(
            username=email,
            email=email,
            password=password,
        )
        return {"user_id": django_user.pk, "email": django_user.email}

    # ──────────────────────────────────────────────
    # Caso de uso: Perfil de cliente
    # ──────────────────────────────────────────────

    def create_customer_profile(self, user_id: int, full_name: str, phone: str) -> CustomerProfile:
        """Crea y persiste el perfil de cliente para el usuario indicado.

        Raises:
            UserDomainError: si el usuario ya tiene un perfil de cliente.
            ValueError: si full_name o phone no son válidos (entidad CustomerProfile).
        """
        if CustomerModel.objects.filter(user_id=user_id).exists():
            raise UserDomainError("Este usuario ya tiene un perfil de cliente.")

        profile = CustomerProfile(full_name=full_name, phone=phone)

        # Obtener o crear el UserModel espejo (puede no existir si el modelo es independiente)
        user_model, _ = UserModel.objects.get_or_create(
            id=user_id,
            defaults={"email": "", "active": True},
        )
        CustomerModel.objects.create(
            user=user_model,
            full_name=profile.full_name,
            phone=profile.phone,
        )
        return profile

    # ──────────────────────────────────────────────
    # Caso de uso: Perfil de cocinero
    # ──────────────────────────────────────────────

    def create_cook_profile(self, user_id: int, name: str, specialty: str) -> CookProfile:
        """Crea y persiste el perfil de cocinero para el usuario indicado.

        Raises:
            UserDomainError: si el usuario ya tiene un perfil de cocinero.
            ValueError: si name o specialty no son válidos (entidad CookProfile).
        """
        if CookModel.objects.filter(user_id=user_id).exists():
            raise UserDomainError("Este usuario ya tiene un perfil de cocinero.")

        profile = CookProfile(name=name, specialty=specialty)

        user_model, _ = UserModel.objects.get_or_create(
            id=user_id,
            defaults={"email": "", "active": True},
        )
        CookModel.objects.create(
            user=user_model,
            name=profile.name,
            specialty=profile.specialty,
        )
        return profile

    # ──────────────────────────────────────────────
    # Caso de uso: Direcciones
    # ──────────────────────────────────────────────

    def list_addresses(self, user_id: int) -> List[Address]:
        """Retorna todas las direcciones del usuario como entidades de dominio."""
        rows = AddressModel.objects.filter(user_id=user_id)
        return [
            Address(
                address_id=None,
                street=row.street,
                city=row.city,
                state=row.state,
                zip_code=row.zip_code,
                is_default=row.is_default,
            )
            for row in rows
        ]

    def add_address(
        self,
        user_id: int,
        street: str,
        city: str,
        state: str,
        zip_code: str,
        is_default: bool = False,
    ) -> Address:
        """Crea y persiste una nueva dirección para el usuario.

        Si is_default=True, desmarca la dirección por defecto anterior.
        Raises:
            ValueError: si algún campo requerido está vacío (entidad Address).
        """
        address = Address(
            street=street,
            city=city,
            state=state,
            zip_code=zip_code,
            is_default=is_default,
        )

        if address.is_default:
            AddressModel.objects.filter(user_id=user_id, is_default=True).update(
                is_default=False
            )

        AddressModel.objects.create(
            user_id=user_id,
            street=address.street,
            city=address.city,
            state=address.state,
            zip_code=address.zip_code,
            is_default=address.is_default,
        )
        return address

    # ──────────────────────────────────────────────
    # Casos de uso heredados (activar / desactivar)
    # ──────────────────────────────────────────────

    def get_by_email(self, email: str) -> Optional[User]:
        return self._repo.get_by_email(email)

    def activate(self, user_id) -> User:
        user = self._repo.get_by_id(user_id)
        if user is None:
            raise ValueError(f"Usuario con id={user_id} no encontrado.")
        user.activate()
        return self._repo.save(user)

    def deactivate(self, user_id) -> User:
        user = self._repo.get_by_id(user_id)
        if user is None:
            raise ValueError(f"Usuario con id={user_id} no encontrado.")
        user.deactivate()
        return self._repo.save(user)