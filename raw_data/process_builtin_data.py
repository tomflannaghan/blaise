from blaise.data.ngram import save_ngram_dist, load_ngram_dist


def process_en_wiki():
    """
    Download https://www.kaggle.com/datasets/ffatty/plain-text-wikipedia-simpleenglish?resource=download and save as en_wiki.txt.
    """
    for n in range(1, 4):
        dist = load_ngram_dist("en_wiki", n)
        save_ngram_dist(dist, "en_wiki", n, save_to_built_in=True)


if __name__ == "__main__":
    process_en_wiki()
