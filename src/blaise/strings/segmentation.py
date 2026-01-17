import math
from blaise.data.worddist import load_word_dist
from pygtrie import CharTrie
import polars as pl


class Segmenter:
    def __init__(
        self,
        word_dist: str | list[str] | dict[str, float],
        n_branch_limit: int | None = None,
    ):
        """
        Initializes a :class:`Segmenter` instance.

        Parameters
        ----------
        word_dist : str | list[str] | dict[str, float]
            The source of word probabilities used for segmentation.
            * If a string, it is interpreted as a word dist name and loaded via
              :func:`load_word_dist`.
            * If a list of strings, each word is assigned an equal probability
              (i.e., a uniform distribution).
            * If a dictionary mapping words to probabilities, the values are
              normalised so that the total probability sums to 1.
        n_branch_limit : int | None, optional
            When set, limits the number of candidate segmentations kept at
            each recursion step to the top ``n_branch_limit`` by score.
            If ``None`` (the default), all candidates are considered.

        Notes
        -----
        The constructor builds a character trie (:class:`pygtrie.CharTrie`) from
        the supplied word distribution to enable efficient prefix checks during
        segmentation.  The trie is stored in ``self._trie`` and the normalised
        distribution in ``self.word_dist``.

        Examples
        --------

        If passed a list, words get equal probability:

        >>> Segmenter(['HELLO', 'WORLD', 'HELL', 'O']).segment('HELLOWORLD')
        shape: (2, 2)
        ┌──────────────┬───────────┐
        │ text         ┆ score     │
        │ ---          ┆ ---       │
        │ str          ┆ f64       │
        ╞══════════════╪═══════════╡
        │ HELL O WORLD ┆ 13.862944 │
        │ HELLO WORLD  ┆ 13.862944 │
        └──────────────┴───────────┘

        If passed a dict, it uses the weights in the dict as probabilities.
        Results are returned with most likely first:

        >>> Segmenter({'HELLO': 0.5, 'WORLD': 0.25, 'HELL': 0.2, 'O': 0.05}).segment('HELLOWORLD')
        shape: (2, 2)
        ┌──────────────┬───────────┐
        │ text         ┆ score     │
        │ ---          ┆ ---       │
        │ str          ┆ f64       │
        ╞══════════════╪═══════════╡
        │ HELLO WORLD  ┆ 10.397208 │
        │ HELL O WORLD ┆ 16.364956 │
        └──────────────┴───────────┘
        """
        if isinstance(word_dist, str):
            word_dist = load_word_dist(word_dist)

        if isinstance(word_dist, list):
            word_dist = {w: 1 / len(word_dist) for w in word_dist}
        elif isinstance(word_dist, dict):
            total = sum(word_dist.values())
            word_dist = {w: p / total for w, p in word_dist.items()}
        else:
            raise TypeError(f"Unsupported type for word_dist: {type(word_dist)}")

        self.word_dist = word_dist
        self.n_branch_limit = n_branch_limit
        self._trie = CharTrie(self.word_dist)

    def segment(self, text: str) -> pl.DataFrame:
        """Segments text into words."""
        return self._segment_impl(text, {}).sort(by="score")

    def _segment_impl(self, text: str, cache) -> pl.DataFrame:
        if len(text) in cache:
            return cache[len(text)]

        if len(text) == 0:
            result = pl.DataFrame(
                [{"text": "", "score": 0}],
                schema={"text": pl.String, "score": pl.Float64},
            )
        else:
            results = []
            for i in range(1, len(text) + 1):
                word = text[:i]
                if not self._trie.has_node(word):
                    break
                if self._trie.has_key(word):
                    p = self._trie[word]
                    sub_result = self._segment_impl(text[i:], cache)
                    sub_result = sub_result.with_columns(
                        text=pl.concat_str(
                            [pl.lit(word), pl.col("text")], separator=" "
                        ),
                        score=pl.col("score") - len(word) * math.log(p),
                    )
                    results.append(sub_result)

            if len(results) == 0:
                result = pl.DataFrame(schema={"text": pl.String, "score": pl.Float64})
            else:
                result = pl.concat(results)

        if self.n_branch_limit is not None and self.n_branch_limit < len(result):
            result = result.bottom_k(self.n_branch_limit, by="score")

        cache[len(text)] = result
        return result.with_columns(text=pl.col("text").str.strip_chars())
