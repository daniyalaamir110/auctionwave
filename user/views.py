from rest_framework import generics, permissions, viewsets
from .serializers import RegisterSerializer, UserReadSerializer, UserEditSerailizer
from common.paginations import StandardResultsSetPagination
from django.contrib.auth.models import User


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This set of views allows getting a specific user or a
    paginated, searchable list of all users
    """

    queryset = User.objects.all()
    serializer_class = UserReadSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.AllowAny]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class EditUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserEditSerailizer
    permission_classes = [permissions.IsAuthenticated]
