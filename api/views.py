from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Product, Bid
from .serializers import CategorySerializer, ProductSerializer, LoginSerializer
from datetime import datetime, timedelta
from django.contrib.auth import login, logout
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


# Create your views here.
class CategoryListApiView(APIView):
    def get(self, request, *args, **kwargs):
        """
        List all categories
        """
        category_list = Category.objects.all()

        serializer = CategorySerializer(category_list, many=True)

        if category_list.__len__() == 0:
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductListApiView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        """
        Get all products
        """
        product_list = Product.objects.all()

        serializer = ProductSerializer(product_list, many=True)

        if product_list.__len__() == 0:
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "title": openapi.Schema(type=openapi.TYPE_STRING, default="Test"),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING, default="test description"
                ),
                "base_price": openapi.Schema(type=openapi.TYPE_INTEGER, default=12000),
                "category_id": openapi.Schema(type=openapi.TYPE_INTEGER, default=1),
                "validity_period": openapi.Schema(
                    description="time in seconds",
                    type=openapi.TYPE_INTEGER,
                    default=1 * 60 * 60,
                ),
            },
            required=[
                "title",
                "description",
                "base_price",
                "category_id",
                "validity_period",
            ],
        ),
        responses=[],
    )
    def post(self, request, *args, **kwargs):
        """
        Create a single new product to advertise for bid
        """
        title = request.data.get("title")
        description = request.data.get("description")
        base_price = request.data.get("base_price")
        category_id = request.data.get("category_id")
        validity_period = int(request.data.get("validity_period"))

        category = Category.objects.get(pk=category_id)
        valid_till = datetime.now() + timedelta(seconds=validity_period)
        creator = request.user.pk
        data = {
            "title": title,
            "description": description,
            "base_price": base_price,
            "valid_till": valid_till,
            "category": category,
            "creator": creator,
        }

        serializer = ProductSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING, default="root"),
                "password": openapi.Schema(type=openapi.TYPE_STRING, default="root"),
            },
            required=["username", "password"],
        ),
        responses={
            202: openapi.Response(description="Logged in successfully"),
            403: openapi.Response(description="Log in failure"),
        },
    )
    def post(self, request):
        serializer = LoginSerializer(
            data=self.request.data, context={"request": self.request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description="Logged out successfully"),
            403: openapi.Response(description="Already out of session"),
        }
    )
    def get(self, request):
        logout(request)
        return Response(None, status=status.HTTP_200_OK)
