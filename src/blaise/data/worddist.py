from collections import Counter
from blaise.strings import normalize_string
from blaise.data.core import load_data, save_data
from blaise.data.corpus import load_corpus


def load_word_dist(name: str, overwrite=False) -> dict[str, float]:
    """
    Loads a word distribution. If `name` is a known corpus name, it'll be generated from that.
    """
    result = None
    try:
        if not overwrite:
            result = load_data("word_dist", f"{name}")
    except FileNotFoundError:
        result = None
    if result is None:
        result = _generate_from_corpus(name, overwrite=overwrite)
    if result is None:
        raise FileNotFoundError(f"No word dist for {name}")
    return result


def _generate_from_corpus(name, overwrite=False):
    try:
        corpus = load_corpus(name, overwrite=overwrite)
    except FileNotFoundError:
        print("No corp")
    print(f"Calculating word distribution from corpus {name}")
    dist = dict(Counter(normalize_string(word) for word in corpus.split()))
    # Some substrings are entirely non-alpha characters so remove these.
    if "" in dist:
        dist.pop("")
    # Normalise word distribution
    total = sum(dist.values())
    dist = {w: n / total for w, n in dist.items()}
    save_word_dist(dist, name)
    print("Saved word distribution")
    return dist


def save_word_dist(dist, name: str, **kwargs):
    save_data(dist, "word_dist", f"{name}", **kwargs)
