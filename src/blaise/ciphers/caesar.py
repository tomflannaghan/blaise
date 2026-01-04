from blaise.ciphers.common import bruteforce_crack
import polars as pl

from blaise.strings import normalize_string


def caesar_encrypt(plaintext: str, key: int) -> str:
    """
    Applies a Caesar shift to plaintext. Positive key value is a right shift, negative is a left shift.
    """
    plaintext = normalize_string(plaintext)
    return "".join(chr(ord("A") + (ord(c) - ord("A") + key) % 26) for c in plaintext)


def caesar_decrypt(ciphertext: str, key: int) -> str:
    """
    Decrypts a Caesar shift that has been applied. Positive key value indicates that it was
    encrypted with a right shift, and negative with a left shift.
    """
    ciphertext = normalize_string(ciphertext)
    return caesar_encrypt(ciphertext, key=-key)


def caesar_crack(
    ciphertext,
    scorer=None,
    top_n=None,
) -> pl.DataFrame:
    """
    Cracks a Caesar shift cipher. It will try all shifts and score them with an ngram scorer.
    """
    return bruteforce_crack(
        ciphertext=ciphertext,
        keys=list(range(26)),
        decrypt=caesar_decrypt,
        scorer=scorer,
        top_n=top_n,
    )
