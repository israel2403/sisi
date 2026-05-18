"""
Validation helper functions for the SISI project.

These functions keep validation logic outside the model classes,
so the code is easier to reuse and test.
"""


def validate_not_empty(value: str, field_name: str) -> str:
    """Validate that a text value is not empty."""
    if value is None or str(value).strip() == "":
        raise ValueError(f"{field_name} cannot be empty.")
    return str(value).strip()


def validate_positive_number(value: float, field_name: str) -> float:
    """Validate that a numeric value is greater than zero."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a valid number.")

    if number <= 0:
        raise ValueError(f"{field_name} must be greater than zero.")

    return number


def validate_non_negative_number(value: float, field_name: str) -> float:
    """Validate that a numeric value is zero or greater."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a valid number.")

    if number < 0:
        raise ValueError(f"{field_name} cannot be negative.")

    return number


def validate_age(value: int) -> int:
    """Validate pediatric patient age."""
    try:
        age = int(value)
    except (TypeError, ValueError):
        raise ValueError("Age must be a valid integer.")

    if age < 0 or age > 17:
        raise ValueError("Age must be between 0 and 17 for a pediatric patient.")

    return age
