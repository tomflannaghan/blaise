"""Tests for the :func:`_remove_repeats` helper used by the Playfair cipher.

The helper is intentionally small but has a few edge‑cases that are easy to
miss: handling the fill character itself, ensuring the result length is
even, and correctly inserting the alternate fill character when the repeat
is the same as the primary fill character.
"""

import pytest

from blaise.ciphers.playfair import Playfair, _to_bigrams


@pytest.mark.parametrize(
    "input_str, fill_char, alt_fill_char, expected",
    [
        # No repeats
        ("ABCDEF", "X", "Q", [("A", "B"), ("C", "D"), ("E", "F")]),
        # Repeat that is broken naturally
        ("BOOK", "X", "Q", [("B", "O"), ("O", "K")]),
        # Repeat that is not broken
        ("OOK", "X", "Q", [("O", "X"), ("O", "K")]),
        # Repeat of the fill_char itself – use alt_fill_char
        ("XX", "X", "Q", [("X", "Q"), ("X", "Q")]),
        # Multiple repeats in a row
        ("AAAA", "X", "Q", [("A", "X")] * 4),
        # Odd length after processing – append fill_char
        ("ABC", "X", "Q", [("A", "B"), ("C", "X")]),
        # Odd length with last char being fill_char – use alt_fill_char
        ("ABX", "X", "Q", [("A", "B"), ("X", "Q")]),
        # Empty string – stays empty
        ("", "X", "Q", []),
        # Single character padded
        ("A", "X", "Q", [("A", "X")]),
    ],
)
def test_to_bigrams(input_str, fill_char, alt_fill_char, expected):
    """Verify that :func:`_remove_repeats` behaves as documented."""
    result = _to_bigrams(input_str, fill_char, alt_fill_char)
    assert result == expected


def test_playfair_encrypt():
    # The wikipedia example
    assert Playfair().encrypt("hide the gold in the tree stump", "playfairexample") == "BMODZBXDNABEKUDMUIXMMOUVIF"


def test_playfair_decrypt():
    # The wikipedia example
    assert Playfair().decrypt("BMODZBXDNABEKUDMUIXMMOUVIF", "playfairexample") == "HIDETHEGOLDINTHETREXESTUMP"

    assert (
        Playfair().decrypt("BMODZBXDNABEKUDMUIXMMOUVIF", "playfairexample", remove_fill=True)
        == "HIDETHEGOLDINTHETREESTUMP"
    )
