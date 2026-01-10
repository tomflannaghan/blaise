import time
from blaise.scores.ngram import calculate_ngrams
from blaise._blaise import calculate_ngrams as rust_calculate_ngrams  # ty: ignore[unresolved-import]
from blaise.strings import normalize_string


SAMPLE = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris 
nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in 
reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla 
pariatur. Excepteur sint occaecat cupidatat non proident, 
sunt in culpa qui officia deserunt mollit anim id est laborum."""


def main():
    text = normalize_string(SAMPLE)
    start = time.time()
    for _ in range(10000):
        calculate_ngrams(text, 3)
    print(time.time() - start)

    start = time.time()
    for _ in range(10000):
        rust_calculate_ngrams(text, 3)
    print(time.time() - start)


if __name__ == "__main__":
    main()
