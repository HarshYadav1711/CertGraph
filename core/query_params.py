"""
Safe query parameter parsing for list APIs.
"""

from rest_framework import status
from rest_framework.response import Response


def parse_optional_int(
    value: str | None, param_name: str
) -> tuple[int | None, Response | None]:
    """
    Parse an optional query parameter as a positive integer.

    Returns (parsed_value, None) on success.
    Returns (None, error_response) when the value is present but invalid.
    When the parameter is absent or empty, returns (None, None).
    """
    if value is None or value == "":
        return None, None
    try:
        parsed = int(value)
    except (ValueError, TypeError):
        return None, Response(
            {param_name: ["Must be a valid integer."]},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if parsed < 1:
        return None, Response(
            {param_name: ["Must be a positive integer."]},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return parsed, None
