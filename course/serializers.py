"""
Serializers for the course app.
"""

from rest_framework import serializers

from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for Course entities.
    """

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "code",
            "description",
            "product",
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

        qs = Course.objects.filter(code__iexact=value)
        if self.instance is not None:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A course with this code already exists.")
        return value

