"""
Views for the vendor app.
"""

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.utils.object_helpers import get_object_or_404_custom
from core.services.certification_path_service import get_vendor_certification_path
from .models import Vendor
from .serializers import VendorSerializer


class VendorListCreateAPIView(APIView):
    """
    List all vendors or create a new vendor.
    """

    @swagger_auto_schema(
        operation_description="List all vendors.",
        responses={
            200: VendorSerializer(many=True),
            400: openapi.Response("Bad request."),
        },
    )
    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new vendor.",
        request_body=VendorSerializer,
        responses={
            201: VendorSerializer,
            400: openapi.Response("Validation error."),
        },
    )
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            vendor = serializer.save()
            return Response(
                VendorSerializer(vendor).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorDetailAPIView(APIView):
    """
    Retrieve, update, partially update, or delete a single vendor.
    """

    def get_object(self, pk: int) -> Vendor:
        return get_object_or_404_custom(Vendor, pk=pk)

    @swagger_auto_schema(
        operation_description="Retrieve a single vendor by ID.",
        responses={
            200: VendorSerializer,
            404: openapi.Response("Vendor not found."),
        },
    )
    def get(self, request, pk: int):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a vendor.",
        request_body=VendorSerializer,
        responses={
            200: VendorSerializer,
            400: openapi.Response("Validation error."),
            404: openapi.Response("Vendor not found."),
        },
    )
    def put(self, request, pk: int):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            vendor = serializer.save()
            return Response(
                VendorSerializer(vendor).data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a vendor.",
        request_body=VendorSerializer,
        responses={
            200: VendorSerializer,
            400: openapi.Response("Validation error."),
            404: openapi.Response("Vendor not found."),
        },
    )
    def patch(self, request, pk: int):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            vendor = serializer.save()
            return Response(
                VendorSerializer(vendor).data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a vendor.",
        responses={
            204: openapi.Response("Vendor deleted."),
            404: openapi.Response("Vendor not found."),
        },
    )
    def delete(self, request, pk: int):
        vendor = self.get_object(pk)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VendorCertificationPathAPIView(APIView):
    """
    Read-only endpoint returning the full certification path for a vendor.

    Structure:
    - Vendor
      - Products
        - Courses
          - Certifications
    """

    @swagger_auto_schema(
        operation_description=(
            "Return the full certification path for a vendor, including "
            "products, courses, and certifications."
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "vendor": openapi.Schema(type=openapi.TYPE_OBJECT),
                    "products": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_OBJECT),
                    ),
                },
            ),
            404: openapi.Response("Vendor not found."),
        },
    )
    def get(self, request, vendor_id: int):
        payload = get_vendor_certification_path(vendor_id=vendor_id)
        return Response(payload, status=status.HTTP_200_OK)


