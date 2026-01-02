import pytest

from blaise.strings import normalize_string, is_alpha, check_is_alpha


def test_normalize_basic_ascii_and_case():
    """Basic ASCII letters and case conversion should work."""
    assert normalize_string("abc") == "ABC"
    assert normalize_string("ABC") == "ABC"
    assert normalize_string("aBcD") == "ABCD"


def test_normalize_numbers_and_punctuation():
    """Numbers and punctuation should be preserved unchanged."""
    assert normalize_string("123!@#") == ""
    assert normalize_string("Hello, World!") == "HELLOWORLD"


def test_normalize_accented_characters():
    """Accented characters should be decomposed to their base ASCII letters."""
    assert normalize_string("áéíóú") == "AEIOU"
    assert normalize_string("Café") == "CAFE"


def test_normalize_non_ascii_removed():
    """Non‑ASCII characters that cannot be decomposed should be removed."""
    assert normalize_string("你好") == ""
    assert normalize_string("Hello, 世界!") == "HELLO"

def test_is_alpha_basic():
    """is_alpha should return True for pure ASCII alphabetic strings."""
    assert is_alpha("abc") is True
    assert is_alpha("ABC") is True
    assert is_alpha("AbC") is True

def test_is_alpha_non_ascii():
    """is_alpha should return False for strings containing non‑ASCII letters."""
    assert is_alpha("áéí") is False
    assert is_alpha("café") is False

def test_is_alpha_non_alpha():
    """is_alpha should return False for strings containing digits or punctuation."""
    assert is_alpha("abc123") is False
    assert is_alpha("hello!") is False

def test_check_is_alpha_raises_on_invalid():
    """check_is_alpha should raise ValueError when the string is not all ASCII letters."""
    with pytest.raises(ValueError):
        check_is_alpha("abc123")
    with pytest.raises(ValueError):
        check_is_alpha("café")

