from typing import cast, Dict, Any

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login

from apps.users.domain.entities.user import User
from apps.users.domain.entities.customer import CustomerProfile
from apps.users.domain.entities.cook import CookProfile
from apps.users.presentation.api.serializers import (
    RegisterUserSerializer,
    CustomerProfileSerializer,
    CookProfileSerializer,
    UserOutputSerializer,
)


# ─── Helper ──────────────────────────────────────────────────────────────────

def _domain_user_from_request(request) -> User:
    """Construye un UserEntity temporal desde el request.user de Django."""
    u = request.user
    return User(
        email=u.email,
        user_id=None,
        active=u.is_active,
    )


# ─── Views ────────────────────────────────────────────────────────────────────

class UserRegisterView(APIView):
    """POST /api/users/register/

    Registra un nuevo usuario usando el sistema de auth de Django.
    No requiere autenticación previa.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = cast(Dict[str, Any], serializer.validated_data)

        from django.contrib.auth import get_user_model
        UserModel = get_user_model()

        if UserModel.objects.filter(username=data["email"]).exists():
            return Response(
                {"error": "Ya existe un usuario con ese email"},
                status=status.HTTP_409_CONFLICT,
            )

        try:
            # Valida reglas de dominio antes de persistir
            domain_user = User(email=str(data["email"]))
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        django_user = UserModel.objects.create_user(
            username=data["email"],
            email=data["email"],
            password=data["password"],
        )

        return Response(
            {"user_id": django_user.pk, "email": django_user.email},
            status=status.HTTP_201_CREATED,
        )


class UserMeView(APIView):
    """GET /api/users/me/

    Retorna la información del usuario autenticado como entidad de dominio.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        domain_user = User(
            email=request.user.email,
            active=request.user.is_active,
        )
        output = UserOutputSerializer(domain_user)
        return Response(output.data, status=status.HTTP_200_OK)


class CustomerProfileView(APIView):
    """POST /api/users/me/customer-profile/

    Añade un perfil de cliente al usuario autenticado.
    Valida las reglas de negocio de CustomerProfile.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CustomerProfileSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = cast(Dict[str, Any], serializer.validated_data)

        try:
            profile = CustomerProfile(
                full_name=str(data["full_name"]),
                phone=str(data["phone"]),
            )
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        return Response(
            {"full_name": profile.full_name, "phone": profile.phone},
            status=status.HTTP_201_CREATED,
        )


class CookProfileView(APIView):
    """POST /api/users/me/cook-profile/

    Añade un perfil de cocinero al usuario autenticado.
    Valida las reglas de negocio de CookProfile.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CookProfileSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = cast(Dict[str, Any], serializer.validated_data)

        try:
            profile = CookProfile(
                name=str(data["name"]),
                specialty=str(data["specialty"]),
            )
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        return Response(
            {"name": profile.name, "specialty": profile.specialty},
            status=status.HTTP_201_CREATED,
        )