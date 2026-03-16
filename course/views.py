"""
Views for the course app.
"""

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.query_params import parse_optional_int
from core.utils.object_helpers import get_object_or_404_custom

from .models import Course
from .serializers import CourseSerializer


class CourseListCreateAPIView(APIView):
    """
    List all courses or create a new course.
    Optional query param: product_id — filter by product primary key.
    """

    @swagger_auto_schema(
        operation_description="List all courses. Optionally filter by product_id.",
        manual_parameters=[
            openapi.Parameter(
                "product_id",
                openapi.IN_QUERY,
                description="Filter courses by product ID.",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: CourseSerializer(many=True),
            400: openapi.Response("Invalid query parameter."),
        },
    )
    def get(self, request):
        product_id_raw = request.query_params.get("product_id")
        product_id, err = parse_optional_int(product_id_raw, "product_id")
        if err is not None:
            return err

        courses = Course.objects.all()
        if product_id is not None:
            courses = courses.filter(product_id=product_id)

        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new course.",
        request_body=CourseSerializer,
        responses={
            201: CourseSerializer,
            400: openapi.Response("Validation error."),
        },
    )
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            course = serializer.save()
            return Response(
                CourseSerializer(course).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailAPIView(APIView):
    """
    Retrieve, update, partially update, or delete a single course.
    """

    def get_object(self, pk: int) -> Course:
        return get_object_or_404_custom(Course, pk=pk)

    @swagger_auto_schema(
        operation_description="Retrieve a single course by ID.",
        responses={
            200: CourseSerializer,
            404: openapi.Response("Course not found."),
        },
    )
    def get(self, request, pk: int):
        course = self.get_object(pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a course.",
        request_body=CourseSerializer,
        responses={
            200: CourseSerializer,
            400: openapi.Response("Validation error."),
            404: openapi.Response("Course not found."),
        },
    )
    def put(self, request, pk: int):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            course = serializer.save()
            return Response(
                CourseSerializer(course).data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a course.",
        request_body=CourseSerializer,
        responses={
            200: CourseSerializer,
            400: openapi.Response("Validation error."),
            404: openapi.Response("Course not found."),
        },
    )
    def patch(self, request, pk: int):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            course = serializer.save()
            return Response(
                CourseSerializer(course).data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a course.",
        responses={
            204: openapi.Response("Course deleted."),
            404: openapi.Response("Course not found."),
        },
    )
    def delete(self, request, pk: int):
        course = self.get_object(pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

