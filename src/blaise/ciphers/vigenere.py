from itertools import zip_longest
from typing import Iterable
from blaise.ciphers.caesar import caesar_crack
from blaise.ciphers.common import rank_results
from blaise.iterators import product_index_ordered
from blaise.strings import check_is_alpha, normalize_string
import polars as pl


def _shift(char: str, shift: int) -> str:
    if char.isupper():
        base = ord("A")
    else:
        base = ord("a")
    return chr((ord(char) - base + shift) % 26 + base)


def _to_key(k: str) -> str:
    check_is_alpha(k)
    return k.upper()


def vigenere_encrypt(plaintext: str, key: str) -> str:
    """Encrypt ``plaintext`` using the Vigenère cipher.

    Parameters
    ----------
    plaintext:
        The text to encrypt.
    key:
        The encryption key. It must consist only of alphabetic
        characters; the function will raise a ``ValueError`` if this
        condition is not met.

    Returns
    -------
    str
        The ciphertext produced by applying the Vigenère shift to each
        alphabetic character of ``plaintext``.
    """
    key = _to_key(key)
    plaintext = normalize_string(plaintext)

    result = []
    key_len = len(key)
    key_index = 0

    for ch in plaintext:
        shift = ord(key[key_index % key_len]) - ord("A")
        result.append(chr(ord("A") + (ord(ch) - ord("A") + shift) % 26))
        key_index += 1

    return "".join(result)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt ``ciphertext`` that was encrypted with the Vigenère cipher.

    Parameters
    ----------
    ciphertext:
        The text to decrypt.
    key:
        The decryption key. It must consist only of alphabetic
        characters; the function will raise a ``ValueError`` if this
        condition is not met.

    Returns
    -------
    str
        The original plaintext recovered from ``ciphertext``.
    """
    key = _to_key(key)
    ciphertext = normalize_string(ciphertext)

    result = []
    key_len = len(key)
    key_index = 0

    for ch in ciphertext:
        shift = ord(key[key_index % key_len]) - ord("A")
        result.append(chr(ord("A") + (ord(ch) - ord("A") - shift) % 26))
        key_index += 1

    return "".join(result)


def vigenere_crack(
    ciphertext: str,
    key_length: int | Iterable[int] = range(3, 8),
    top_n=10,
    n_trials: int = 1000,
    scorer=None,
) -> pl.DataFrame:
    """
    Cracks Vigenere. Returns the top n results in pairs of (key, plaintext).
    """
    vigenere_results = []
    if not isinstance(key_length, int):
        for key_len in key_length:
            vigenere_results += vigenere_crack(
                ciphertext,
                key_len,
                top_n=top_n,
                scorer=scorer,
                n_trials=n_trials,
            ).to_dicts()
    else:
        caesar_results = []
        for i in range(key_length):
            subsec = ciphertext[i::key_length]
            # Note ngram here is 1 because the sections are not contiguous - only letter freqs are usable.
            caesar_results.append(caesar_crack(subsec, scorer=scorer).to_dicts())

        for combo in product_index_ordered(*caesar_results):
            plaintext = "".join(
                sum(zip_longest(*[res["plaintext"] for res in combo], fillvalue=""), ())
            )
            key = "".join(chr(ord("A") + res["key"]) for res in combo)
            vigenere_results.append({"key": key, "plaintext": plaintext})
            if len(vigenere_results) > n_trials:
                break

    df = pl.from_dicts(vigenere_results)
    return rank_results(df, scorer=scorer, top_n=top_n)
