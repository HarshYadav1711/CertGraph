"""
Views for the vendor_product_mapping app.
"""

from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import VendorProductMapping
from .serializers import VendorProductMappingSerializer


class VendorProductMappingListCreateAPIView(APIView):
    """
    List all vendor-product mappings or create a new mapping.
    """

    def get(self, request):
        mappings = VendorProductMapping.objects.all()
        serializer = VendorProductMappingSerializer(mappings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VendorProductMappingSerializer(data=request.data)
        if serializer.is_valid():
            mapping = serializer.save()
            return Response(
                VendorProductMappingSerializer(mapping).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorProductMappingDetailAPIView(APIView):
    """
    Retrieve, update, partially update, or delete a single vendor-product mapping.
    """

    def get_object(self, pk: int) -> VendorProductMapping:
        try:
            return VendorProductMapping.objects.get(pk=pk)
        except VendorProductMapping.DoesNotExist as exc:
            raise Http404("Vendor-product mapping not found.") from exc

    def get(self, request, pk: int):
        mapping = self.get_object(pk)
        serializer = VendorProductMappingSerializer(mapping)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk: int):
        mapping = self.get_object(pk)
        serializer = VendorProductMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            mapping = serializer.save()
            return Response(
                VendorProductMappingSerializer(mapping).data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk: int):
        mapping = self.get_object(pk)
        serializer = VendorProductMappingSerializer(
            mapping, data=request.data, partial=True
        )
        if serializer.is_valid():
            mapping = serializer.save()
            return Response(
                VendorProductMappingSerializer(mapping).data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk: int):
        mapping = self.get_object(pk)
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

