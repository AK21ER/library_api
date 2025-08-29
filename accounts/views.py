from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
User = get_user_model()

from .serializers import (
    RegisterSerializer,
    PublicUserSerializer,
    UserCreateUpdateSerializer,
)
from .permissions import IsSelfOrAdmin

# POST /api/accounts/register/
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# POST /api/accounts/login/  (wrapper around SimpleJWT)
class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

# /api/users/  (list for admin, self CRUD via /users/me/ or /users/{id})
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return UserCreateUpdateSerializer
        return PublicUserSerializer

    def get_permissions(self):
        if self.action in ["list", "destroy"]:
            return [permissions.IsAdminUser()]
        if self.action in ["retrieve", "update", "partial_update"]:
            return [permissions.IsAuthenticated(), IsSelfOrAdmin()]
        return [permissions.IsAuthenticated()]

    def get_object(self):
        if self.kwargs.get("pk") == "me":
            return self.request.user
        return super().get_object()

