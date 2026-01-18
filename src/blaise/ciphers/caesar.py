import polars as pl

from blaise.ciphers.common import Cipher
from blaise.scores.base import Scorer
from blaise.strings import normalize_string


class Caesar(Cipher):
    """
    The Caesar Cipher is the simplest of ciphers, where each letter is shifted by a
    fixed amount in either direction.
    Wikipedia page: https://en.wikipedia.org/wiki/Caesar_cipher
    """

    def encrypt(self, plaintext: str, key: int) -> str:
        """
        Applies a Caesar shift to plaintext. Positive key value is a right shift, negative is a left shift.
        """
        plaintext = normalize_string(plaintext)
        return "".join(chr(ord("A") + (ord(c) - ord("A") + key) % 26) for c in plaintext)

    def decrypt(self, ciphertext: str, key: int) -> str:
        """
        Decrypts a Caesar shift that has been applied. Positive key value indicates that it was
        encrypted with a right shift, and negative with a left shift.
        """
        ciphertext = normalize_string(ciphertext)
        return self.encrypt(ciphertext, key=-key)

    def crack(self, ciphertext, scorer: Scorer | None = None, top_n: int | None = None) -> pl.DataFrame:
        """
        Cracks a Caesar shift cipher. It will try all shifts and score them with an ngram scorer.

        Parameters
        ----------
        ciphertext : str
            The ciphertext to crack.
        scorer : optional
            Scorer function to evaluate plaintext candidates.
        top_n : optional
            Number of top results to return.

        Example
        -------

        >>> Caesar().crack('EBIILTLOIA', top_n=3)
        shape: (3, 3)
        ┌─────┬────────────┬──────────┐
        │ key ┆ plaintext  ┆ score    │
        │ --- ┆ ---        ┆ ---      │
        │ i64 ┆ str        ┆ f64      │
        ╞═════╪════════════╪══════════╡
        │ 23  ┆ HELLOWORLD ┆ 1.535752 │
        │ 8   ┆ WTAADLDGAS ┆ 1.995915 │
        │ 19  ┆ LIPPSASVPH ┆ 2.051054 │
        └─────┴────────────┴──────────┘

        """
        return self.bruteforce_crack(
            ciphertext=ciphertext,
            keys=list(range(26)),
            scorer=scorer,
            top_n=top_n,
        )
