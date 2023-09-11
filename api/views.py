from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Product, Bid
from .serializers import CategorySerializer, ProductSerializer
from datetime import datetime, timedelta

# Create your views here.
class CategoryListApiView(APIView):

    def get(self, request, *args, **kwargs):
        """
            List all categories
        """
        category_list = Category.objects.all()

        serializer = CategorySerializer(category_list, many=True)

        if (category_list.__len__() == 0):

            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ProductListApiView(APIView):

    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        """
            Get all products
        """
        product_list = Product.objects.all()

        serializer = ProductSerializer(product_list, many=True)

        if (product_list.__len__() == 0):

            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


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
            "creator": creator
        }

        serializer = ProductSerializer(data=data)

        if serializer.is_valid():
            
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
