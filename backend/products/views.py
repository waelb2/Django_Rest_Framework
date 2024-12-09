from django.urls.exceptions import Http404
from rest_framework import generics, status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer

# Create your views here.


class ProductDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    fields = ["title"]


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        title = serializer.validated_data.get("title")
        content = serializer.validated_data.get("content")
        if not content:
            content = title
        serializer.save(content=content)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def product_view(request, pk=None, *args, **kargs):
    method = request.method
    if method == "GET":
        if pk is not None:
            # list detailed product
            qs = Product.objects.filter(pk=pk)
            if not qs.exists():
                return Response(
                    {"Error": f"Product with id: {pk} Not Found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            data = ProductSerializer(qs.first()).data
            return Response(data, status=status.HTTP_200_OK)
        # list all products
        qs = Product.objects.all()
        data = ProductSerializer(
            qs,
            many=True,
        ).data
        return Response(data)

    elif method == "POST":
        # create product
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            content = serializer.validated_data.get("content")
            if not content:
                content = serializer.validated_data.get("title")
            serializer.save(content=content)

            return Response(
                {"Message": "Product added successfully"},
                status=status.HTTP_201_CREATED,
            )

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(
            {"Error": "Invalid http method"}, status=status.HTTP_400_BAD_REQUEST
        )
