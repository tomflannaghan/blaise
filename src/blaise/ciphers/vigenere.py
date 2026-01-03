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
        The text to encrypt. Non‑alphabetic characters are preserved
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
        The text to decrypt. Non‑alphabetic characters are preserved
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
