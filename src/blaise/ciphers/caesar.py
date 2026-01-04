from blaise.scores.ngram import ngram_top_n
from blaise.strings import normalize_string


def caesar_encrypt(plaintext: str, key: int, is_norm=False) -> str:
    """
    Applies a Caesar shift to plaintext. Positive key value is a right shift, negative is a left shift.
    """
    if not is_norm:
        plaintext = normalize_string(plaintext)
    return "".join(chr(ord("A") + (ord(c) - ord("A") + key) % 26) for c in plaintext)


def caesar_decrypt(ciphertext: str, key: int, is_norm=False) -> str:
    """
    Decrypts a Caesar shift that has been applied. Positive key value indicates that it was
    encrypted with a right shift, and negative with a left shift.
    """
    return caesar_encrypt(ciphertext, key=-key, is_norm=is_norm)


def caesar_crack(
    ciphertext,
    ngram_dist="en_wiki",
    ngram_n=2,
    is_norm=False,
    top_n=26,
) -> list[tuple[int, str]]:
    """
    Cracks a Caesar shift cipher. It will try all shifts and score them with an ngram scorer.
    Returns (key, plaintext) pairs in order of score.
    """
    results = [
        (shift, caesar_decrypt(ciphertext, key=shift, is_norm=is_norm))
        for shift in range(26)
    ]
    return ngram_top_n(
        results, top_n=top_n, expected=ngram_dist, n=ngram_n, key=lambda x: x[1]
    )
