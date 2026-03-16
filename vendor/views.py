"""
Views for the vendor app.
"""

from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Vendor
from .serializers import VendorSerializer
from course.models import Course
from course_certification_mapping.models import CourseCertificationMapping
from product.models import Product
from product_course_mapping.models import ProductCourseMapping
from certification.models import Certification
from vendor_product_mapping.models import VendorProductMapping


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
        try:
            return Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist as exc:
            raise Http404("Vendor not found.") from exc

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

    def get_vendor(self, vendor_id: int) -> Vendor:
        try:
            return Vendor.objects.get(pk=vendor_id)
        except Vendor.DoesNotExist as exc:
            raise Http404("Vendor not found.") from exc

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
        vendor = self.get_vendor(vendor_id)

        # Products linked via VendorProductMapping
        product_mappings = VendorProductMapping.objects.filter(parent=vendor).select_related(
            "child"
        )
        products = [mapping.child for mapping in product_mappings]
        product_ids = [p.id for p in products]

        # Courses linked via ProductCourseMapping
        product_course_mappings = ProductCourseMapping.objects.filter(
            parent_id__in=product_ids
        ).select_related("child")
        courses = [m.child for m in product_course_mappings]
        course_ids = [c.id for c in courses]

        # Certifications linked via CourseCertificationMapping
        course_cert_mappings = CourseCertificationMapping.objects.filter(
            parent_id__in=course_ids
        ).select_related("child")
        certifications = [m.child for m in course_cert_mappings]

        # Index courses and certifications by their parents
        courses_by_product: dict[int, list[Course]] = {}
        for mapping in product_course_mappings:
            courses_by_product.setdefault(mapping.parent_id, []).append(mapping.child)

        certs_by_course: dict[int, list[Certification]] = {}
        for mapping in course_cert_mappings:
            certs_by_course.setdefault(mapping.parent_id, []).append(mapping.child)

        # Build nested structure
        vendor_data = VendorSerializer(vendor).data

        products_payload = []
        for product in products:
            product_dict = {
                "id": product.id,
                "name": product.name,
                "code": product.code,
                "description": product.description,
                "is_active": product.is_active,
            }

            product_courses = courses_by_product.get(product.id, [])
            courses_payload = []
            for course in product_courses:
                course_dict = {
                    "id": course.id,
                    "name": course.name,
                    "code": course.code,
                    "description": course.description,
                    "is_active": course.is_active,
                }

                course_certs = certs_by_course.get(course.id, [])
                certs_payload = [
                    {
                        "id": cert.id,
                        "name": cert.name,
                        "code": cert.code,
                        "description": cert.description,
                        "is_active": cert.is_active,
                    }
                    for cert in course_certs
                ]

                course_dict["certifications"] = certs_payload
                courses_payload.append(course_dict)

            product_dict["courses"] = courses_payload
            products_payload.append(product_dict)

        payload = {
            "vendor": vendor_data,
            "products": products_payload,
        }

        return Response(payload, status=status.HTTP_200_OK)


