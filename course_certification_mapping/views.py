"""
Views for the course_certification_mapping app.
"""

from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CourseCertificationMapping
from .serializers import CourseCertificationMappingSerializer


class CourseCertificationMappingListCreateAPIView(APIView):
    """
    List all course-certification mappings or create a new mapping.
    """

    def get(self, request):
        mappings = CourseCertificationMapping.objects.all()
        serializer = CourseCertificationMappingSerializer(mappings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

    def get(self, request, pk: int):
        mapping = self.get_object(pk)
        serializer = CourseCertificationMappingSerializer(mapping)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

    def delete(self, request, pk: int):
        mapping = self.get_object(pk)
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

