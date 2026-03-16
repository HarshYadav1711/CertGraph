"""
Miscellaneous project-level API views.
"""

from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckAPIView(APIView):
    """
    Simple health check to verify the API server is running.
    """

    authentication_classes: list = []
    permission_classes: list = []

    def get(self, request):
        return Response(
            {
                "status": "ok",
                "service": "CertGraph API",
            }
        )

