from collections import Counter


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
