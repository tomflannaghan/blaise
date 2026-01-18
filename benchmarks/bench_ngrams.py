import time

from blaise.scores.ngram import NGramScorer, _PyNGramScorer
from blaise.strings import normalize_string

SAMPLE = """Lorem ipsum dolor sit amet, consectetur adipiscing elit,
sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in
reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
pariatur. Excepteur sint occaecat cupidatat non proident,
sunt in culpa qui officia deserunt mollit anim id est laborum."""


def main():
    texts = [normalize_string(SAMPLE)] * 1000
    rs_s = NGramScorer(3, "en_wiki")
    py_s = _PyNGramScorer(3, "en_wiki")
    start = time.time()
    for t in texts:
        res = py_s.score(t)
    print("Python:", time.time() - start, res)

    start = time.time()
    for t in texts:
        res = rs_s.score(t)
    print("Rust:", time.time() - start, res)


if __name__ == "__main__":
    main()
