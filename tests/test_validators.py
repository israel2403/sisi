"""
Unit tests for validators.

These tests focus only on validation helper functions.
They do not test the GUI, repository, or service logic.
"""

import pytest

from validators import (
    validate_age,
    validate_non_negative_number,
    validate_not_empty,
    validate_positive_number,
)


# -------------------------------------------------------------------------------
# Tests for validate_not_empty
# -------------------------------------------------------------------------------
def test_validate_not_emptyf_returns_stripeed_string():
    # Checks that a valid string is returned without surrouding spaces.
    result = validate_not_empty("  Juan Pérez  ", "Name")

    assert result == "Juan Pérez"


def test_validate_not_empty_accepts_non_string_values_as_text():
    # Checks that non-string values are converted to string if not empty.
    result = validate_not_empty("123", "Code")

    assert result == "123"


@pytest.mark.parametrize("invalid_value", [None, "", "  ", "\t", "\n"])
def test_validate_not_empty_raises_value_error_for_empty_values(invalid_value):
    # Checks that empty values are rejected.
    with pytest.raises(ValueError):
        validate_not_empty(invalid_value, "Name")


# -------------------------------------------------------------------------------
# Tests for validate_positive_number
# -------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "value, expected",
    [
        (1, 1.0),
        ("1", 1.0),
        ("2.5", 2.5),
        (3.75, 3.75),
        (" 4.5", 4.5),
    ],
)
def test_validate_positive_number_returns_float_for_valid_values(value, expected):
    # Chekcs that valid positive numeric values are converted to float.
    result = validate_positive_number(value, "weight")

    assert result == expected
    assert isinstance(result, float)


@pytest.mark.parametrize("invalid_value", [0, "0", -1, "-2.5"])
def test_validate_positive_number_raises_value_error_for_zero_or_negative_values(
    invalid_value,
):
    # Checks that zero and negative numbers are rejected.
    with pytest.raises(ValueError):
        validate_positive_number(invalid_value, "weight")


@pytest.mark.parametrize("invalid_value", ["abc", "", "   ", None])
def test_validate_positive_number_raises_value_error_for_non_numeric_values(
    invalid_value,
):
    # Checks taht values that cannot be converted to float are rejected.
    with pytest.raises(ValueError):
        validate_positive_number(invalid_value, "weight")


# -------------------------------------------------------------------------------
# Tests for validate_positive_number
# -------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "value, expected",
    [
        (0, 0.0),
        ("0", 0.0),
        (1, 1.0),
        ("2.5", 2.5),
        (" 3.75 ", 3.75),
    ],
)
def test_validate_non_negative_number_returns_float_for_valid_values(value, expected):
    # Checks that zero and positive numbers are accepted.
    result = validate_non_negative_number(value, "Height")

    assert result == expected
    assert isinstance(result, float)


@pytest.mark.parametrize("invalid_value", [-1, "-1", -0.5, "-0.5"])
def test_validate_non_negative_number_raises_value_error_for_negative_values(
    invalid_value,
):
    # Checks that negative numbers are rejected.
    with pytest.raises(ValueError):
        validate_non_negative_number(invalid_value, "Height")


@pytest.mark.parametrize("invalid_value", ["abc", "", "   ", None])
def test_validate_non_negative_number_raises_value_error_for_non_numeric_values(
    invalid_value,
):
    # Checks that values that cannot be converted to float are rejected.
    with pytest.raises(ValueError):
        validate_non_negative_number(invalid_value, "Height")


# ---------------------------------------------------------
# Tests for validate_age
# ---------------------------------------------------------


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, 0),
        ("0", 0),
        (1, 1),
        ("5", 5),
        (17, 17),
        ("17", 17),
        (" 10 ", 10),
    ],
)
def test_validate_age_returns_int_for_valid_pediatric_ages(value, expected):
    # Checks that ages from 0 to 17 are accepted and converted to int.
    result = validate_age(value)

    assert result == expected
    assert isinstance(result, int)


@pytest.mark.parametrize("invalid_value", [-1, "-1", 18, "18", 100])
def test_validate_age_raises_value_error_for_out_of_range_ages(invalid_value):
    # Checks that ages less than 0 or greater than 17 are rejected.
    with pytest.raises(ValueError):
        validate_age(invalid_value)


@pytest.mark.parametrize("invalid_value", ["abc", "", "   ", None])
def test_validate_age_raises_value_error_for_non_integer_values(invalid_value):
    # Checks that values that cannot be converted to int are rejected.
    with pytest.raises(ValueError):
        validate_age(invalid_value)
