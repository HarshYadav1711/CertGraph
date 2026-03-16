"""
Views for the course_certification_mapping app.
"""

from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CourseCertificationMapping
from .serializers import CourseCertificationMappingSerializer


class CourseCertificationMappingListCreateAPIView(APIView):
    """
    List all course-certification mappings or create a new mapping.
    """

    @swagger_auto_schema(
        operation_description="List all course-certification mappings.",
        responses={
            200: CourseCertificationMappingSerializer(many=True),
            400: openapi.Response("Bad request."),
        },
    )
    def get(self, request):
        mappings = CourseCertificationMapping.objects.all()
        serializer = CourseCertificationMappingSerializer(mappings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new course-certification mapping.",
        request_body=CourseCertificationMappingSerializer,
        responses={
            201: CourseCertificationMappingSerializer,
            400: openapi.Response("Validation error."),
        },
    )
    def post(self, request):
        serializer = CourseCertificationMappingSerializer(data=request.data)
        if serializer.is_valid():
            mapping = serializer.save()
            return Response(
                CourseCertificationMappingSerializer(mapping).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseCertificationMappingDetailAPIView(APIView):
    """
    Retrieve, update, partially update, or delete a single course-certification
    mapping.
    """

    def get_object(self, pk: int) -> CourseCertificationMapping:
        try:
            return CourseCertificationMapping.objects.get(pk=pk)
        except CourseCertificationMapping.DoesNotExist as exc:
            raise Http404("Course-certification mapping not found.") from exc

    @swagger_auto_schema(
        operation_description="Retrieve a course-certification mapping by ID.",
        responses={
            200: CourseCertificationMappingSerializer,
            404: openapi.Response("Course-certification mapping not found."),
        },
    )
    def get(self, request, pk: int):
        mapping = self.get_object(pk)
        serializer = CourseCertificationMappingSerializer(mapping)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a course-certification mapping.",
        request_body=CourseCertificationMappingSerializer,
        responses={
            200: CourseCertificationMappingSerializer,
            400: openapi.Response("Validation error."),
            404: openapi.Response("Course-certification mapping not found."),
        },
    )
    def put(self, request, pk: int):
        mapping = self.get_object(pk)
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            mapping = serializer.save()
            return Response(
                CourseCertificationMappingSerializer(mapping).data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a course-certification mapping.",
        request_body=CourseCertificationMappingSerializer,
        responses={
            200: CourseCertificationMappingSerializer,
            400: openapi.Response("Validation error."),
            404: openapi.Response("Course-certification mapping not found."),
        },
    )
    def patch(self, request, pk: int):
        mapping = self.get_object(pk)
        serializer = CourseCertificationMappingSerializer(
            mapping, data=request.data, partial=True
        )
        if serializer.is_valid():
            mapping = serializer.save()
            return Response(
                CourseCertificationMappingSerializer(mapping).data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a course-certification mapping.",
        responses={
            204: openapi.Response("Course-certification mapping deleted."),
            404: openapi.Response("Course-certification mapping not found."),
        },
    )
    def delete(self, request, pk: int):
        mapping = self.get_object(pk)
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

