"""
Serializers for the certification app.
"""

from rest_framework import serializers

from .models import Certification


class CertificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Certification entities.
    """

    class Meta:
        model = Certification
        fields = [
            "id",
            "name",
            "code",
            "description",
            "course",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_name(self, value: str) -> str:
        if not value:
            raise serializers.ValidationError("Name is required.")
        return value

    def validate_code(self, value: str) -> str:
        if not value:
            raise serializers.ValidationError("Code is required.")

        qs = Certification.objects.filter(code__iexact=value)
        if self.instance is not None:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "A certification with this code already exists."
            )
        return value

