"""
Views for the product_course_mapping app.
"""

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.utils.object_helpers import get_object_or_404_custom
from .models import ProductCourseMapping
from .serializers import ProductCourseMappingSerializer


class ProductCourseMappingListCreateAPIView(APIView):
    """
    List all product-course mappings or create a new mapping.
    """

    @swagger_auto_schema(
        operation_description="List all product-course mappings.",
        responses={
            200: ProductCourseMappingSerializer(many=True),
            400: openapi.Response("Bad request."),
        },
    )
    def get(self, request):
        mappings = ProductCourseMapping.objects.all()
        serializer = ProductCourseMappingSerializer(mappings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new product-course mapping.",
        request_body=ProductCourseMappingSerializer,
        responses={
            201: ProductCourseMappingSerializer,
            400: openapi.Response("Validation error."),
        },
    )
    def post(self, request):
        serializer = ProductCourseMappingSerializer(data=request.data)
        if serializer.is_valid():
            mapping = serializer.save()
            return Response(
                ProductCourseMappingSerializer(mapping).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCourseMappingDetailAPIView(APIView):
    """
    Retrieve, update, partially update, or delete a single product-course mapping.
    """

    def get_object(self, pk: int) -> ProductCourseMapping:
        return get_object_or_404_custom(ProductCourseMapping, pk=pk)

    @swagger_auto_schema(
        operation_description="Retrieve a product-course mapping by ID.",
        responses={
            200: ProductCourseMappingSerializer,
            404: openapi.Response("Product-course mapping not found."),
        },
    )
    def get(self, request, pk: int):
        mapping = self.get_object(pk)
        serializer = ProductCourseMappingSerializer(mapping)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a product-course mapping.",
        request_body=ProductCourseMappingSerializer,
        responses={
            200: ProductCourseMappingSerializer,
            400: openapi.Response("Validation error."),
            404: openapi.Response("Product-course mapping not found."),
        },
    )
    def put(self, request, pk: int):
        mapping = self.get_object(pk)
        serializer = ProductCourseMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            mapping = serializer.save()
            return Response(
                ProductCourseMappingSerializer(mapping).data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a product-course mapping.",
        request_body=ProductCourseMappingSerializer,
        responses={
            200: ProductCourseMappingSerializer,
            400: openapi.Response("Validation error."),
            404: openapi.Response("Product-course mapping not found."),
        },
    )
    def patch(self, request, pk: int):
        mapping = self.get_object(pk)
        serializer = ProductCourseMappingSerializer(
            mapping, data=request.data, partial=True
        )
        if serializer.is_valid():
            mapping = serializer.save()
            return Response(
                ProductCourseMappingSerializer(mapping).data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a product-course mapping.",
        responses={
            204: openapi.Response("Product-course mapping deleted."),
            404: openapi.Response("Product-course mapping not found."),
        },
    )
    def delete(self, request, pk: int):
        mapping = self.get_object(pk)
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

