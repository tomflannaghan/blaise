from itertools import zip_longest
from typing import Iterable
from blaise.ciphers.caesar import caesar_crack
from blaise.ciphers.common import _rank_results
from blaise.iterators import product_index_ordered
from blaise.strings import check_is_alpha, normalize_string
import polars as pl


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

    Examples
    --------

    >>> vigenere_encrypt("HELLO", "FOO")
    'MSZQC'
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

    Examples
    --------

    >>> vigenere_decrypt("MSZQC", "FOO")
    'HELLO'
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
    Cracks a Vigenère cipher.

    Parameters
    ----------
    ciphertext : str
        The ciphertext to crack. Note that non-alphabetic characters are
        ignored.
    key_length : int | Iterable[int], optional
        The length(s) of the key to try.  If an integer is supplied,
        the function will attempt to crack a key of that exact length.
        If an iterable is supplied, the function will iterate over
        each length in the iterable.  The default is ``range(3, 8)``,
        which tries key lengths 3 through 7.
    top_n : int, optional
        The maximum number of results to return.  Results are sorted
        by the provided ``scorer``.
    n_trials : int, optional
        The maximum number of key combinations to evaluate for each
        ``key_length``.  This limits the search space for long keys.
    scorer : Scorer, optional
        The scorer to use for assessing the quality of the output
        plaintext.

    Returns
    -------
    polars.DataFrame
        A DataFrame with columns ``key`` and ``plaintext`` containing
        the best candidate keys and their corresponding decrypted
        plaintexts.  The DataFrame is sorted by score in descending
        order and limited to ``top_n`` rows.

    Notes
    -----
    The function works by splitting the ciphertext into ``key_length``
    interleaved subsequences and cracking each subsequence with a
    Caesar-cipher cracker.  The resulting candidate keys are then
    combined using a Cartesian product to form full Vigenère keys
    in order of likelihood based on frequency analysis of each
    interleaved Caesar shift. The search is truncated after
    ``n_trials`` combinations to keep runtime reasonable for long keys.

    Examples
    --------

    Here is an example with a relatively short ciphertext. Note that
    the correct decrypt is not the top result because the ciphertext
    is too short for very accurate decryption.

    >>> from blaise.ciphers.vigenere import vigenere_crack
    >>> vigenere_crack("DLCFMEORCBIASTFOV", key_length=3, top_n=3)
    shape: (3, 3)
    ┌─────┬───────────────────┬──────────┐
    │ key ┆ plaintext         ┆ score    │
    │ --- ┆ ---               ┆ ---      │
    │ str ┆ str               ┆ f64      │
    ╞═════╪═══════════════════╪══════════╡
    │ OAY ┆ PLERMGARENICETHAV ┆ 1.146352 │
    │ KEY ┆ THEVIGENERECIPHER ┆ 1.161679 │
    │ OEY ┆ PHERIGANENECEPHAR ┆ 1.162718 │
    └─────┴───────────────────┴──────────┘
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
    return _rank_results(df, scorer=scorer, top_n=top_n)
