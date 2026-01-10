from blaise.strings.ngram import calculate_ngrams
from blaise.strings import normalize_string
from blaise.data.core import load_data, save_data
from blaise.data.corpus import load_corpus


def load_ngram_dist(name: str, n: int) -> dict[str, float]:
    try:
        return load_data("ngram_dist", f"{name}_{n}")
    except FileNotFoundError:
        # Attempt to calculate from corpus.
        corpus = normalize_string(load_corpus(name))
        print(f"Calculating ngram distribution from corpus {name}")
        dist = calculate_ngrams(corpus, n)
        save_ngram_dist(dist, name, n)
        print("Saved ngram distribution")
        return dist


def save_ngram_dist(dist, name: str, n: int, **kwargs):
    save_data(dist, "ngram_dist", f"{name}_{n}", **kwargs)
