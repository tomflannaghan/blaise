import math

from blaise import _blaise  # ty: ignore[unresolved-import]
from blaise.data.ngram import load_ngram_dist
from blaise.scores.base import Scorer
from blaise.strings.ngram import calculate_ngrams


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
    return -math.log(sum((dist1.get(k, 0) * dist2.get(k, 0)) ** 0.5 for k in dist1.keys() & dist2.keys()))


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
