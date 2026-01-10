from collections import Counter
import math

from blaise.data import load_data, save_data
from blaise.scores.base import Scorer
from blaise import _blaise  # ty: ignore[unresolved-import]


def calculate_ngrams(text: str, n: int) -> dict[str, float]:
    """
    Compute the n-gram frequencies of a string.

    The function slides a window of length n over the input string and
    counts how many times each distinct n-character substring occurs.
    The frequencies are returned as a dictionary mapping each n-gram to
    its relative frequency (count divided by the total number of
    n-grams).

    >>> calculate_ngrams("ABCABC", 3)
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
            (dist1.get(k, 0) * dist2.get(k, 0)) ** 0.5
            for k in dist1.keys() & dist2.keys()
        )
    )


def load_ngram_dist(name: str, n: int) -> dict[str, float]:
    return load_data("ngram_dist", f"{name}_{n}")


def save_ngram_dist(dist, name: str, n: int, **kwargs):
    save_data(dist, "ngram_dist", f"{name}_{n}", **kwargs)


class _PyNGramScorer(Scorer):
    """
    Scores N-Grams using the Bhattacharyya distance - reference python impl.
    """

    def __init__(self, n: int, expected: dict[str, float] | str) -> None:
        super().__init__()
        if isinstance(expected, str):
            expected = load_ngram_dist(expected, n)
        self.expected_dist = expected
        self.n = n

    def score(self, text: str) -> float:
        return bd_score(self.expected_dist, calculate_ngrams(text, self.n))


class NGramScorer(Scorer):
    """
    Scores N-Grams using the Bhattacharyya distance
    """

    def __init__(self, n: int, expected: dict[str, float] | str) -> None:
        super().__init__()
        if isinstance(expected, str):
            expected = load_ngram_dist(expected, n)
        self.expected_dist = expected
        self._rs_dist = _blaise.to_dist(self.expected_dist)
        self.n = n

    def score(self, text: str) -> float:
        return _blaise.bd_score(text, self.n, self._rs_dist)
