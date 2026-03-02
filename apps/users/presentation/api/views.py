from typing import cast, Dict, Any

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

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

class UserRegisterView(APIView):
    """POST /api/users/register/ — Registra un usuario nuevo."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if not serializer.is_valid():
            # 400: email malformado, password demasiado corta…
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = cast(Dict[str, Any], serializer.validated_data)

        from django.contrib.auth import get_user_model
        UserModel = get_user_model()

        if UserModel.objects.filter(username=data["email"]).exists():
            # 409: conflicto — ya existe un usuario con ese email (unicidad violada)
            return Response(
                {"error": "Ya existe un usuario con ese email"},
                status=status.HTTP_409_CONFLICT,
            )

        try:
            # Validación de reglas de dominio antes de persistir
            User(email=str(data["email"]))
        except ValueError as exc:
            # 400: el email no cumple la regla de negocio (sin @, etc.)
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        django_user = UserModel.objects.create_user(
            username=data["email"],
            email=data["email"],
            password=data["password"],
        )

        # 201: recurso usuario creado
        return Response(
            {"user_id": django_user.pk, "email": django_user.email},
            status=status.HTTP_201_CREATED,
        )


class UserMeView(APIView):
    """GET /api/users/me/ — Info del usuario autenticado."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        domain_user = User(
            email=request.user.email,
            active=request.user.is_active,
        )
        # 200: lectura exitosa
        return Response(UserOutputSerializer(domain_user).data, status=status.HTTP_200_OK)


class CustomerProfileView(APIView):
    """POST /api/users/me/customer-profile/ — Añade perfil de cliente."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CustomerProfileSerializer(data=request.data)
        if not serializer.is_valid():
            # 400: full_name vacío, teléfono demasiado corto…
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = cast(Dict[str, Any], serializer.validated_data)

        try:
            profile = CustomerProfile(
                full_name=str(data["full_name"]),
                phone=str(data["phone"]),
            )
        except ValueError as exc:
            # 400: regla de negocio violada dentro de CustomerProfile
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        # 201: perfil creado
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
            # 400: name o specialty vacíos
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = cast(Dict[str, Any], serializer.validated_data)

        try:
            profile = CookProfile(
                name=str(data["name"]),
                specialty=str(data["specialty"]),
            )
        except ValueError as exc:
            # 400: regla de negocio violada dentro de CookProfile
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        # 201: perfil creado
        return Response(
            {"name": profile.name, "specialty": profile.specialty},
            status=status.HTTP_201_CREATED,
        )