from blaise.strings import check_is_alpha


def _shift(char: str, shift: int) -> str:
    """Shift a single alphabetic character by `shift` positions."""
    if char.isupper():
        base = ord("A")
    else:
        base = ord("a")
    return chr((ord(char) - base + shift) % 26 + base)


def _to_key(k: str) -> str:
    check_is_alpha(k)
    return k.upper()


def encrypt_vigenere(plaintext: str, key: str) -> str:
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


def decrypt_vigenere(ciphertext: str, key: str) -> str:
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
