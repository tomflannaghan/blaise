from itertools import zip_longest
from typing import Iterable
from blaise.ciphers.caesar import caesar_crack
from blaise.iterators import product_index_ordered
from blaise.scores.ngram import ngram_top_n
from blaise.strings import check_is_alpha


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
        The text to encrypt. Non-alphabetic characters are preserved
        unchanged.
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

    result = []
    key_len = len(key)
    key_index = 0

    for ch in plaintext:
        if ch.isalpha():
            shift = ord(key[key_index % key_len]) - ord("A")
            result.append(_shift(ch, shift))
            key_index += 1
        else:
            result.append(ch)

    return "".join(result)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt ``ciphertext`` that was encrypted with the Vigenère cipher.

    Parameters
    ----------
    ciphertext:
        The text to decrypt. Non-alphabetic characters are preserved
        unchanged.
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

    result = []
    key_len = len(key)
    key_index = 0

    for ch in ciphertext:
        if ch.isalpha():
            shift = ord(key[key_index % key_len]) - ord("A")
            result.append(_shift(ch, -shift))
            key_index += 1
        else:
            result.append(ch)

    return "".join(result)


def vigenere_crack(
    ciphertext: str,
    key_length: int | Iterable[int] = range(3, 8),
    top_n=10,
    n_trials: int = 1000,
    ngram_dist="en_wiki",
    ngram_n=2,
) -> list[tuple[str, str]]:
    """
    Cracks Vigenere. Returns the top n results in pairs of (key, plaintext).
    """
    vigenere_results = []
    if isinstance(key_length, Iterable):
        for key_len in key_length:
            vigenere_results += vigenere_crack(
                ciphertext,
                key_len,
                top_n=top_n,
                ngram_dist=ngram_dist,
                ngram_n=ngram_n,
                n_trials=n_trials,
            )
    else:
        caesar_results = []
        for i in range(key_length):
            subsec = ciphertext[i::key_length]
            # Note ngram here is 1 because the sections are not contiguous - only letter freqs are usable.
            caesar_results.append(
                caesar_crack(subsec, ngram_n=1, ngram_dist=ngram_dist, is_norm=True)
            )

        for combo in product_index_ordered(*caesar_results):
            plaintext = "".join(
                sum(zip_longest(*[res[1] for res in combo], fillvalue=""), ())
            )
            key = "".join(chr(ord("A") + res[0]) for res in combo)
            vigenere_results.append((key, plaintext))
            if len(vigenere_results) > n_trials:
                break

    return ngram_top_n(
        vigenere_results,
        n=ngram_n,
        expected=ngram_dist,
        top_n=top_n,
        key=lambda x: x[1],
    )
