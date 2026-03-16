"""
Views for the product app.
"""

from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.query_params import parse_optional_int

from .models import Product
from .serializers import ProductSerializer


class ProductListCreateAPIView(APIView):
    """
    List all products or create a new product.
    Optional query param: vendor_id — filter by vendor primary key.
    """

    @swagger_auto_schema(
        operation_description="List all products. Optionally filter by vendor_id.",
        manual_parameters=[
            openapi.Parameter(
                "vendor_id",
                openapi.IN_QUERY,
                description="Filter products by vendor ID.",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: ProductSerializer(many=True),
            400: openapi.Response("Invalid query parameter."),
        },
    )
    def get(self, request):
        vendor_id_raw = request.query_params.get("vendor_id")
        vendor_id, err = parse_optional_int(vendor_id_raw, "vendor_id")
        if err is not None:
            return err

        products = Product.objects.all()
        if vendor_id is not None:
            products = products.filter(vendor_id=vendor_id)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new product.",
        request_body=ProductSerializer,
        responses={
            201: ProductSerializer,
            400: openapi.Response("Validation error."),
        },
    )
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(
                ProductSerializer(product).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPIView(APIView):
    """
    Retrieve, update, partially update, or delete a single product.
    """

    def get_object(self, pk: int) -> Product:
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist as exc:
            raise Http404("Product not found.") from exc

    @swagger_auto_schema(
        operation_description="Retrieve a single product by ID.",
        responses={
            200: ProductSerializer,
            404: openapi.Response("Product not found."),
        },
    )
    def get(self, request, pk: int):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a product.",
        request_body=ProductSerializer,
        responses={
            200: ProductSerializer,
            400: openapi.Response("Validation error."),
            404: openapi.Response("Product not found."),
        },
    )
    def put(self, request, pk: int):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(
                ProductSerializer(product).data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a product.",
        request_body=ProductSerializer,
        responses={
            200: ProductSerializer,
            400: openapi.Response("Validation error."),
            404: openapi.Response("Product not found."),
        },
    )
    def patch(self, request, pk: int):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            product = serializer.save()
            return Response(
                ProductSerializer(product).data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a product.",
        responses={
            204: openapi.Response("Product deleted."),
            404: openapi.Response("Product not found."),
        },
    )
    def delete(self, request, pk: int):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

