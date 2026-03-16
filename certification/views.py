"""
Views for the certification app.
"""

from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.query_params import parse_optional_int

from .models import Certification
from .serializers import CertificationSerializer


class CertificationListCreateAPIView(APIView):
    """
    List all certifications or create a new certification.
    Optional query param: course_id — filter by course primary key.
    """

    @swagger_auto_schema(
        operation_description="List all certifications. Optionally filter by course_id.",
        manual_parameters=[
            openapi.Parameter(
                "course_id",
                openapi.IN_QUERY,
                description="Filter certifications by course ID.",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: CertificationSerializer(many=True),
            400: openapi.Response("Invalid query parameter."),
        },
    )
    def get(self, request):
        course_id_raw = request.query_params.get("course_id")
        course_id, err = parse_optional_int(course_id_raw, "course_id")
        if err is not None:
            return err

        certifications = Certification.objects.all()
        if course_id is not None:
            certifications = certifications.filter(course_id=course_id)

        serializer = CertificationSerializer(certifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new certification.",
        request_body=CertificationSerializer,
        responses={
            201: CertificationSerializer,
            400: openapi.Response("Validation error."),
        },
    )
    def post(self, request):
        serializer = CertificationSerializer(data=request.data)
        if serializer.is_valid():
            certification = serializer.save()
            return Response(
                CertificationSerializer(certification).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CertificationDetailAPIView(APIView):
    """
    Retrieve, update, partially update, or delete a single certification.
    """

    def get_object(self, pk: int) -> Certification:
        try:
            return Certification.objects.get(pk=pk)
        except Certification.DoesNotExist as exc:
            raise Http404("Certification not found.") from exc

    @swagger_auto_schema(
        operation_description="Retrieve a single certification by ID.",
        responses={
            200: CertificationSerializer,
            404: openapi.Response("Certification not found."),
        },
    )
    def get(self, request, pk: int):
        certification = self.get_object(pk)
        serializer = CertificationSerializer(certification)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a certification.",
        request_body=CertificationSerializer,
        responses={
            200: CertificationSerializer,
            400: openapi.Response("Validation error."),
            404: openapi.Response("Certification not found."),
        },
    )
    def put(self, request, pk: int):
        certification = self.get_object(pk)
        serializer = CertificationSerializer(certification, data=request.data)
        if serializer.is_valid():
            certification = serializer.save()
            return Response(
                CertificationSerializer(certification).data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a certification.",
        request_body=CertificationSerializer,
        responses={
            200: CertificationSerializer,
            400: openapi.Response("Validation error."),
            404: openapi.Response("Certification not found."),
        },
    )
    def patch(self, request, pk: int):
        certification = self.get_object(pk)
        serializer = CertificationSerializer(
            certification, data=request.data, partial=True
        )
        if serializer.is_valid():
            certification = serializer.save()
            return Response(
                CertificationSerializer(certification).data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a certification.",
        responses={
            204: openapi.Response("Certification deleted."),
            404: openapi.Response("Certification not found."),
        },
    )
    def delete(self, request, pk: int):
        certification = self.get_object(pk)
        certification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

