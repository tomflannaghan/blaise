from abc import ABC, abstractmethod
from typing import Any

import polars as pl

from blaise.scores.base import Scorer, as_scorer


class Cipher(ABC):
    @abstractmethod
    def encrypt(self, plaintext: str, key: Any) -> str:
        """Encrypts a string using the cipher."""

    @abstractmethod
    def decrypt(self, ciphertext: str, key: Any) -> str:
        """Decrypts a string using the cipher."""

    def bruteforce_crack(
        self,
        ciphertext: str,
        keys: list,
        scorer: Scorer | None = None,
        top_n: int | None = None,
    ) -> pl.DataFrame:
        """
        A bruteforce attempt to crack a cipher by trying all keys in a list. Returns a dataframe of the
        top n results (or all of the results if not specified), ordered by score (best first).
        """
        df = pl.from_dict({"key": keys})
        df = df.with_columns(
            plaintext=pl.col("key").map_elements(
                lambda key: self.decrypt(ciphertext=ciphertext, key=key),
                return_dtype=pl.String,
            )
        )
        return _rank_results(df, scorer=scorer, top_n=top_n)


def _rank_results(df: pl.DataFrame, scorer: Scorer | None = None, top_n: int | None = None):
    scorer = as_scorer(scorer)
    df = df.with_columns(
        score=pl.col("plaintext").map_elements(lambda plaintext: scorer.score(plaintext), return_dtype=pl.Float64)
    )
    return df.bottom_k(top_n if top_n is not None else len(df), by="score")
