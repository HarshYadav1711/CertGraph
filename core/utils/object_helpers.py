"""
Helpers for retrieving model instances with consistent error handling.
"""

from typing import Type

from django.db.models import Model
from rest_framework.exceptions import NotFound


def get_object_or_404_custom(model: Type[Model], **filters: object) -> Model:
    """
    Retrieve a single object matching the given filters or raise NotFound.

    This is similar to Django's get_object_or_404 but returns a DRF
    NotFound exception so that API responses follow DRF's error format.
    """
    try:
        return model.objects.get(**filters)
    except model.DoesNotExist as exc:  # type: ignore[attr-defined]
        model_name = getattr(model, "__name__", "Object")
        # Compose a simple, clear message. We don't echo raw filters to avoid
        # leaking implementation details.
        message = f"{model_name} not found."
        raise NotFound(detail=message) from exc

