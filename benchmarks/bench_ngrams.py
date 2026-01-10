import time
from blaise.scores.ngram import NGramScorer, load_ngram_dist
from blaise._blaise import bh_score_many  # ty: ignore[unresolved-import]
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
    dist = load_ngram_dist("en_wiki", 3)
    s = NGramScorer(3, expected=dist)
    start = time.time()
    for t in texts:
        s.score(t)
    print(time.time() - start)

    start = time.time()
    bh_score_many(texts, 3, dist)
    print(time.time() - start)

    start = time.time()
    for t in texts:
        bh_score_many([t], 3, dist)
    print(time.time() - start)


if __name__ == "__main__":
    main()
