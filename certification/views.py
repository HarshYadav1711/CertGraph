"""
Views for the certification app.
"""

from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Certification
from .serializers import CertificationSerializer


class CertificationListCreateAPIView(APIView):
    """
    List all certifications or create a new certification.
    """

    def get(self, request):
        certifications = Certification.objects.all()
        serializer = CertificationSerializer(certifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

    def get(self, request, pk: int):
        certification = self.get_object(pk)
        serializer = CertificationSerializer(certification)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

    def delete(self, request, pk: int):
        certification = self.get_object(pk)
        certification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

