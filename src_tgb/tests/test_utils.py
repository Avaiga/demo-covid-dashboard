import pytest
from utils import to_text


def test_to_text_with_int():
    assert to_text(1000) == "1 000"


def test_to_text_with_float():
    assert to_text(12345.67) == "12 345"  # float gets cast to int


def test_to_text_with_string_number():
    assert to_text("9999") == "9 999"


def test_to_text_with_invalid_string():
    assert to_text("hello") == "hello"


def test_to_text_with_none():
    assert to_text(None) == "No information"


def test_to_text_with_empty_string():
    assert to_text("") == "No information"
