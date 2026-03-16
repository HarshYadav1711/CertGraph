"""
Views for the course app.
"""

from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.query_params import parse_optional_int

from .models import Course
from .serializers import CourseSerializer


class CourseListCreateAPIView(APIView):
    """
    List all courses or create a new course.
    Optional query param: product_id — filter by product primary key.
    """

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
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist as exc:
            raise Http404("Course not found.") from exc

    def get(self, request, pk: int):
        course = self.get_object(pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

    def delete(self, request, pk: int):
        course = self.get_object(pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

