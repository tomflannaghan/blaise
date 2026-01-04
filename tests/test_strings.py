import pytest

from blaise.strings import normalize_string, is_alpha, check_is_alpha, restore_string


class TestNormalize:
    def test_normalize_basic_ascii_and_case(self):
        """Basic ASCII letters and case conversion should work."""
        assert normalize_string("abc") == "ABC"
        assert normalize_string("ABC") == "ABC"
        assert normalize_string("aBcD") == "ABCD"

    def test_normalize_numbers_and_punctuation(self):
        """Numbers and punctuation should be preserved unchanged."""
        assert normalize_string("123!@#") == ""
        assert normalize_string("Hello, World!") == "HELLOWORLD"

    def test_normalize_accented_characters(self):
        """Accented characters should be decomposed to their base ASCII letters."""
        assert normalize_string("áéíóú") == "AEIOU"
        assert normalize_string("Café") == "CAFE"

    def test_normalize_non_ascii_removed(self):
        """Non‑ASCII characters that cannot be decomposed should be removed."""
        assert normalize_string("你好") == ""
        assert normalize_string("Hello, 世界!") == "HELLO"


class TestIsAlpha:
    def test_is_alpha_basic(self):
        """is_alpha should return True for pure ASCII alphabetic strings."""
        assert is_alpha("abc") is True
        assert is_alpha("ABC") is True
        assert is_alpha("AbC") is True

    def test_is_alpha_non_ascii(self):
        """is_alpha should return False for strings containing non‑ASCII letters."""
        assert is_alpha("áéí") is False
        assert is_alpha("café") is False

    def test_is_alpha_non_alpha(self):
        """is_alpha should return False for strings containing digits or punctuation."""
        assert is_alpha("abc123") is False
        assert is_alpha("hello!") is False

    def test_check_is_alpha_raises_on_invalid(self):
        """check_is_alpha should raise ValueError when the string is not all ASCII letters."""
        with pytest.raises(ValueError):
            check_is_alpha("abc123")
        with pytest.raises(ValueError):
            check_is_alpha("café")


class TestRestoreString:
    """Tests for the restore_string function."""

    def test_basic_insertion_of_nonletters(self):
        """Non‑letter characters should be inserted back into the result."""
        input_str = "Hello, World!"
        # Normalized result string (letters only, uppercase)
        result_str = "KINGSCROSS"
        expected = "KINGS, CROSS!"
        assert restore_string(input_str, result_str) == expected

    def test_no_nonletters(self):
        """If there are no non-letters, the result string is returned unchanged."""
        input_str = "HELLO"
        result_str = "ABCDE"
        assert restore_string(input_str, result_str) == result_str

    def test_length_mismatch_raises(self):
        """If the number of letters differs, a ValueError is raised."""
        input_str = "HELLO"
        result_str = "ABCDEF"
        with pytest.raises(ValueError):
            restore_string(input_str, result_str)

    def test_rest_has_nonletters_raises(self):
        """If the remaining part of the input contains non‑letters, a ValueError is raised."""
        input_str = "HELLO1"
        result_str = "ABCDE"
        assert restore_string(input_str, result_str) == "ABCDE1"

    def test_case_not_restored(self):
        """The function does not restore the original case of letters."""
        input_str = "Hello"
        result_str = "ABCDE"
        assert restore_string(input_str, result_str) == "ABCDE"
