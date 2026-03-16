"""
Views for the product_course_mapping app.
"""

from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ProductCourseMapping
from .serializers import ProductCourseMappingSerializer


class ProductCourseMappingListCreateAPIView(APIView):
    """
    List all product-course mappings or create a new mapping.
    """

    def get(self, request):
        mappings = ProductCourseMapping.objects.all()
        serializer = ProductCourseMappingSerializer(mappings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        try:
            return ProductCourseMapping.objects.get(pk=pk)
        except ProductCourseMapping.DoesNotExist as exc:
            raise Http404("Product-course mapping not found.") from exc

    def get(self, request, pk: int):
        mapping = self.get_object(pk)
        serializer = ProductCourseMappingSerializer(mapping)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

    def delete(self, request, pk: int):
        mapping = self.get_object(pk)
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

