import pytest

from blaise.scores.ngram import calculate_ngrams


def test_calculate_ngrams_basic() -> None:
    """Test basic n‑gram frequency calculation.

    The example from the module docstring is used as a reference.
    """
    text = "ABCABC"
    expected = {"ABC": 0.5, "BCA": 0.25, "CAB": 0.25}
    result = calculate_ngrams(text, 3)
    assert result == expected


def test_calculate_ngrams_unigrams_and_bigrams() -> None:
    """Check unigrams and bigrams for a short string."""
    text = "ABCD"
    # Unigrams
    unigrams = calculate_ngrams(text, 1)
    assert unigrams == {"A": 0.25, "B": 0.25, "C": 0.25, "D": 0.25}
    # Bigrams
    bigrams = calculate_ngrams(text, 2)
    assert bigrams == {
        "AB": 0.3333333333333333,
        "BC": 0.3333333333333333,
        "CD": 0.3333333333333333,
    }


def test_calculate_ngrams_edge_cases() -> None:
    """Test edge cases: n <= 0, n > len(text) and len(text) < n."""
    with pytest.raises(ValueError):
        calculate_ngrams("ABC", 0)
    # n greater than length returns empty dict
    assert calculate_ngrams("ABC", 4) == {}
    # len(text) < n also returns empty dict
    assert calculate_ngrams("AB", 3) == {}
