from typing import cast, Dict, Any

from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.users.application.services.user_service import UserService
from apps.users.domain.entities.user import User
from apps.users.domain.exceptions import UserDomainError
from apps.users.infrastructure.models.cook_model import CookModel
from apps.users.infrastructure.models.customer_model import CustomerModel
from apps.users.infrastructure.models.user_model import UserModel
from apps.users.infrastructure.repositories.django_user_repository import DjangoUserRepository
from apps.users.presentation.api.serializers import (
    RegisterUserSerializer,
    LoginUserSerializer,
    CustomerProfileSerializer,
    CookProfileSerializer,
    AddressSerializer,
    AddressOutputSerializer,
    UserOutputSerializer,
)


def _build_service() -> UserService:
    """Construye el servicio con sus dependencias inyectadas."""
    return UserService(repo=DjangoUserRepository())


def _ui_role_for_user(user) -> str:
    """Rol de interfaz (solo presentación): customer | chef | operations."""
    try:
        if user.is_staff or user.is_superuser:
            return "operations"
        email = (user.email or "").strip().lower()
        if not email:
            return "customer"
        try:
            profile_user = UserModel.objects.get(email__iexact=email)
        except UserModel.DoesNotExist:
            return "customer"
        if CookModel.objects.filter(user=profile_user).exists():
            return "chef"
        if CustomerModel.objects.filter(user=profile_user).exists():
            return "customer"
        return "customer"
    except Exception:
        return "customer"


class UserRegisterView(APIView):
    """POST /api/users/register/ — Registra un usuario nuevo."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = cast(Dict[str, Any], serializer.validated_data)
        service = _build_service()

        try:
            result = service.register_user(
                email=str(data["email"]),
                password=str(data["password"]),
            )
        except UserDomainError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_409_CONFLICT)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    """POST /api/users/login/ - Crea una sesion autenticada en Django."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = cast(Dict[str, Any], serializer.validated_data)
        email = str(data["email"]).strip().lower()
        password = str(data["password"])
        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response(
                {"error": _("Credenciales incorrectas. Verifica tu email y contraseña.")},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        login(request, user)
        return Response(
            {
                "email": user.email,
                "active": user.is_active,
                "ui_role": _ui_role_for_user(user),
            },
            status=status.HTTP_200_OK,
        )


class UserLogoutView(APIView):
    """POST /api/users/logout/ - Cierra la sesion autenticada."""

    permission_classes = [AllowAny]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserMeView(APIView):
    """GET /api/users/me/ — Info del usuario autenticado."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        domain_user = User(
            email=request.user.email,
            active=request.user.is_active,
        )
        return Response(UserOutputSerializer(domain_user).data, status=status.HTTP_200_OK)


class CustomerProfileView(APIView):
    """POST /api/users/me/customer-profile/ — Añade perfil de cliente."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CustomerProfileSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = cast(Dict[str, Any], serializer.validated_data)
        service = _build_service()

        try:
            profile = service.create_customer_profile(
                user_id=request.user.pk,
                full_name=str(data["full_name"]),
                phone=str(data["phone"]),
            )
        except UserDomainError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_409_CONFLICT)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"full_name": profile.full_name, "phone": profile.phone},
            status=status.HTTP_201_CREATED,
        )


class CookProfileView(APIView):
    """POST /api/users/me/cook-profile/ — Añade perfil de cocinero."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CookProfileSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = cast(Dict[str, Any], serializer.validated_data)
        service = _build_service()

        try:
            profile = service.create_cook_profile(
                user_id=request.user.pk,
                name=str(data["name"]),
                specialty=str(data["specialty"]),
            )
        except UserDomainError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_409_CONFLICT)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"name": profile.name, "specialty": profile.specialty},
            status=status.HTTP_201_CREATED,
        )


class UserAddressListCreateView(APIView):
    """
    GET  /api/users/me/addresses/ — Lista las direcciones del usuario autenticado.
    POST /api/users/me/addresses/ — Añade una nueva dirección al usuario autenticado.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = _build_service()
        addresses = service.list_addresses(user_id=request.user.pk)
        return Response(
            AddressOutputSerializer(addresses, many=True).data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = cast(Dict[str, Any], serializer.validated_data)
        service = _build_service()

        try:
            address = service.add_address(
                user_id=request.user.pk,
                street=data["street"],
                city=data["city"],
                state=data["state"],
                zip_code=data["zip_code"],
                is_default=data.get("is_default", False),
            )
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            AddressOutputSerializer(address).data,
            status=status.HTTP_201_CREATED,
        )
