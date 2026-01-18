from blaise.ciphers.common import Cipher
from blaise.strings import check_is_alpha, normalize_string


class Playfair(Cipher):
    """
    Wikipedia page: https://en.wikipedia.org/wiki/Playfair_cipher.
    """

    def __init__(self, fill_char="X", alt_fill_char="Q", missing_letter: str = "J->I"):
        self._missing_letter, self._missing_letter_replacement = missing_letter.split("->")
        self._alphabet = [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if c != self._missing_letter]
        self._fill_char = fill_char
        self._alt_fill_char = alt_fill_char

    def encrypt(self, plaintext: str, key: str) -> str:
        """
        Encrypts using the Playfair cipher.

        >>> Playfair().encrypt("hide the gold in the tree stump", "playfairexample")
        'BMODZBXDNABEKUDMUIXMMOUVIF'
        """
        key = _to_key(key, self._alphabet)
        plaintext = normalize_string(plaintext).replace(self._missing_letter, self._missing_letter_replacement)
        return _playfair_encrypt(
            _to_bigrams(plaintext, fill_char=self._fill_char, alt_fill_char=self._alt_fill_char),
            key,
        )

    def decrypt(self, ciphertext: str, key: str, remove_fill=False) -> str:
        """
        Decrypts using the Playfair cipher. Will fail if:
        - Any bigram is a repeat
        - Any character in the ciphertext isn't present in the alphabet provided

        >>> Playfair().decrypt("BMODZBXDNABEKUDMUIXMMOUVIF", "playfairexample")
        'HIDETHEGOLDINTHETREXESTUMP'

        Optionally there is a heuristic approach to removing fill characters. It
        isn't perfect - will be caught out by a legitimate EX EC for example - would
        remove the X in that case.

        >>> Playfair().decrypt("BMODZBXDNABEKUDMUIXMMOUVIF", "playfairexample", remove_fill=True)
        'HIDETHEGOLDINTHETREESTUMP'

        """
        key = _to_key(key, self._alphabet)
        ciphertext = normalize_string(ciphertext)
        if len(ciphertext) % 2 != 0:
            raise ValueError(f"Requires even length ciphertext: {ciphertext}")

        # Reverse the key - it's equivalent to decrypting
        plaintext = _playfair_encrypt(zip(ciphertext[::2], ciphertext[1::2]), key[::-1])
        if remove_fill:
            plaintext = _remove_fill(plaintext, fill_char=self._fill_char, alt_fill_char=self._alt_fill_char)

        return plaintext


def _playfair_encrypt(bigrams, key) -> str:
    result = []
    for c1, c2 in bigrams:
        if c1 == c2:
            raise ValueError(f"No repeated letter bigrams allowed: {c1, c2}")
        i1 = key.find(c1)
        i2 = key.find(c2)
        if i1 < 0 or i2 < 0:
            raise ValueError(f"Character not in key: {c1, c2} not in {key}")
        x1, y1 = _index_to_xy(i1)
        x2, y2 = _index_to_xy(i2)
        x1, y1, x2, y2 = _exchange_xy(x1, y1, x2, y2)
        result.append(key[x1 + 5 * y1])
        result.append(key[x2 + 5 * y2])

    return "".join(result)


def _to_key(key: str, alphabet) -> str:
    check_is_alpha(key)
    key = key.upper()

    unseen = set(alphabet)
    result = []
    for c in key:
        if c in unseen:
            result.append(c)
            unseen.remove(c)

    return "".join(result + sorted(unseen))


def _index_to_xy(i):
    return i % 5, i // 5


def _exchange_xy(x1, y1, x2, y2):
    if x1 == x2:
        return x1, (y1 + 1) % 5, x2, (y2 + 1) % 5
    elif y1 == y2:
        return (x1 + 1) % 5, y1, (x2 + 1) % 5, y2
    else:
        return x2, y1, x1, y2


def _to_bigrams(string: str, fill_char: str = "X", alt_fill_char: str = "Q") -> list[tuple[str, str]]:
    """
    Converts string into bigrams. The bigrams cannot be repeated letters. If they are
    we add an additional letter, the fill_char, to the message.
    """
    result = []

    i = 0
    while i < len(string):
        c1 = string[i]
        i += 1
        if i == len(string):
            result.append((c1, (fill_char if c1 != fill_char else alt_fill_char)))
            break

        c2 = string[i]
        if c1 == c2:
            result.append((c1, (fill_char if c1 != fill_char else alt_fill_char)))
        else:
            result.append((c1, c2))
            i += 1

    return result


def _remove_fill(plaintext, fill_char, alt_fill_char):
    """Heuristically removes fill characters added by _to_bigrams. Approximate inverse."""
    if len(plaintext) % 2 != 0:
        raise ValueError(f"Expected even length text: {plaintext}")

    bigrams = list(zip(plaintext[::2], plaintext[1::2]))
    result = []
    for i in range(len(bigrams)):
        b = bigrams[i]
        # Repeating the final bigram gives generally sensible behaviour.
        next_b = b if i == len(bigrams) - 1 else bigrams[i + 1]
        if b[1] == fill_char and b[0] == next_b[0]:
            result.append(b[0])
        elif b[1] == alt_fill_char and b[0] == fill_char and next_b[0] == fill_char:
            result.append(b[0])
        else:
            result.extend(b)
    return "".join(result)
