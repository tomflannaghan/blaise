from blaise.ciphers.common import bruteforce_crack
import polars as pl


def caesar_encrypt(plaintext: str, key: int) -> str:
    """
    Applies a Caesar shift to plaintext. Positive key value is a right shift, negative is a left shift.
    """
    return "".join(chr(ord("A") + (ord(c) - ord("A") + key) % 26) for c in plaintext)


def caesar_decrypt(ciphertext: str, key: int) -> str:
    """
    Decrypts a Caesar shift that has been applied. Positive key value indicates that it was
    encrypted with a right shift, and negative with a left shift.
    """
    return caesar_encrypt(ciphertext, key=-key)


def caesar_crack(
    ciphertext,
    scorer=None,
    top_n=None,
) -> pl.DataFrame:
    """
    Cracks a Caesar shift cipher. It will try all shifts and score them with an ngram scorer.
    Returns (key, plaintext) pairs in order of score.
    """
    return bruteforce_crack(
        ciphertext=ciphertext,
        keys=list(range(26)),
        decrypt=caesar_decrypt,
        scorer=scorer,
        top_n=top_n,
    )
