from collections import Counter
import math
from typing import Callable, Iterable

from blaise.data import load_data, save_data


def calculate_ngrams(text: str, n: int) -> dict[str, float]:
    """
    Compute the n-gram frequencies of a string.

    The function slides a window of length n over the input string and
    counts how many times each distinct n-character substring occurs.
    The frequencies are returned as a dictionary mapping each n-gram to
    its relative frequency (count divided by the total number of
    n-grams).

    >>> calculate_ngrams("ABCABC")
    {'ABC': 0.5, 'BCA': 0.25, 'CAB': 0.25}
    """
    if n <= 0:
        raise ValueError("n must be >= 1")
    if len(text) < n:
        return {}
    # Generate all n-grams
    ngrams = [text[i : i + n] for i in range(len(text) - n + 1)]
    counts = Counter(ngrams)
    total = sum(counts.values())
    return {gram: count / total for gram, count in counts.items()}


def bd_score(dist1: dict[str, float], dist2: dict[str, float]) -> float:
    """
    Calculates the Bhattacharyya distance (https://en.wikipedia.org/wiki/Bhattacharyya_distance)
    between two n-gram distributions.
    """
    if len(dist1) == 0 or len(dist2) == 0:
        raise ValueError("Cannot calculate BD score on empty distributions")
    k1 = next(iter(dist1.keys()))
    k2 = next(iter(dist2.keys()))
    if len(k1) != len(k2):
        raise ValueError("Distributions are for different length ngrams")
    return -math.log(
        sum(
            (dist1.get(k, 0) * dist2.get(k, 0)) ** 2
            for k in dist1.keys() | dist2.keys()
        )
    )


def ngram_score(text: str, n: int, expected: dict[str, float] | str) -> float:
    if isinstance(expected, str):
        expected = load_ngram_dist(expected, n)
    return bd_score(expected, calculate_ngrams(text, n))


def ngram_top_n(
    iterable: Iterable,
    n: int,
    expected: dict[str, float] | str,
    top_n: int = 10,
    key: Callable = lambda x: x,
) -> list:
    ordered = sorted(
        iterable, key=lambda x: ngram_score(key(x), n, expected=expected))
    return ordered[:top_n]


def load_ngram_dist(name: str, n: int) -> dict[str, float]:
    return load_data("ngram_dist", f"{name}_{n}")


def save_ngram_dist(dist, name: str, n: int, **kwargs):
    save_data(dist, "ngram_dist", f"{name}_{n}", **kwargs)
