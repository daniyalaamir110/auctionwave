from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    CreateAPIView,
)
from django.db.models.query import Q
from rest_framework.filters import SearchFilter
from .serializers import (
    UserSerializer,
    UserUpdatePasswordSerializer,
    UsernameSuggestionSerializer,
    EmailAvailabilitySerializer,
    UsernameAvailabilitySerializer,
)
from common.paginations import StandardResultsSetPagination
from django.contrib.auth.models import User


class UserListView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter]
    search_fields = ["first_name", "last_name", "email", "username"]


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserMeDetailView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    @action(detail=False, methods=["GET"], url_path="")
    def retrieve(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=HTTP_200_OK)

    @action(detail=False, methods=["PATCH"], url_path="")
    def update(self, request):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserUpdatePasswordView(UpdateAPIView):
    serializer_class = UserUpdatePasswordSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=["PUT"], detail=False)
    def update(self, request):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(None, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UsernameSuggestionView(CreateAPIView):
    serializer_class = UsernameSuggestionSerializer
    permission_classes = [AllowAny]

    @action(methods="POST", detail=False)
    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            first_name = serializer.validated_data.get("first_name")
            last_name = serializer.validated_data.get("last_name")

            # Generate username suggestions
            suggestions = self.generate_username_suggestions(first_name, last_name)

            return Response(suggestions, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def generate_username_suggestions(self, first_name, last_name):
        first_name = first_name.lower()
        last_name = last_name.lower()

        prefixes = [
            f"{first_name[0]}{last_name}",
            f"{first_name}{last_name[0]}",
            f"{first_name}.{last_name}",
        ]

        existing_users = User.objects.filter(
            Q(username__startswith=prefixes[0])
            | Q(username__iexact=prefixes[0])
            | Q(username__startswith=prefixes[1])
            | Q(username__iexact=prefixes[1])
            | Q(username__startswith=prefixes[2])
            | Q(username__iexact=prefixes[2])
        )

        suggestions = []

        for prefix in prefixes:
            x = 0
            attempts = 0
            active = True
            while active and attempts < 10:
                if (existing_users.filter(username=f"{prefix}{x}")).exists():
                    x += 1
                    attempts += 1
                else:
                    suggestions.append(f"{prefix}{x}")
                    active = False

        return suggestions


class UsernameAvailabilityView(CreateAPIView):
    serializer_class = UsernameAvailabilitySerializer

    @action(methods="POST", detail=False)
    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get("username")

            available = not (User.objects.filter(username=username).exists())

            return Response(available, status=HTTP_200_OK)

        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class EmailAvailabilityView(CreateAPIView):
    serializer_class = EmailAvailabilitySerializer

    @action(methods="POST", detail=False)
    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get("email")

            available = not (User.objects.filter(email=email).exists())

            return Response(available, status=HTTP_200_OK)

        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
