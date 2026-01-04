

import os
from blaise.scores.ngram import calculate_ngrams, save_ngram_dist
from blaise.strings import normalize_string


def process_en_wiki():
    """
    Download https://www.kaggle.com/datasets/ffatty/plain-text-wikipedia-simpleenglish?resource=download and save as en_wiki.txt.
    """
    all_data = open(os.path.join(os.path.dirname(__file__), 'en_wiki.txt')).read()
    all_data_norm = normalize_string(all_data)
    for n in [1, 2, 3]:
        dist = calculate_ngrams(all_data_norm, n)
        save_ngram_dist(dist, "en_wiki", n=n, save_to_built_in=True)


if __name__ == '__main__':
    process_en_wiki()
