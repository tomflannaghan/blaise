import re
import unicodedata


def normalize_string(s: str) -> str:
    """
    Normalize a Unicode string to uppercase ASCII letters A-Z.

    The function performs the following steps:
    1. Normalizes the string to NFKD form, decomposing characters.
    2. Encodes to ASCII, ignoring characters that cannot be represented.
    3. Decodes back to a string.
    4. Converts the result to uppercase.
    5. Removes any characters that are not A-Z.

    Parameters
    ----------
    s: str
            The input Unicode string.

    Returns
    -------
    str
            The normalized string containing only uppercase ASCII letters.
    """
    # Decompose Unicode characters
    decomposed = unicodedata.normalize("NFKD", s)
    # Encode to ASCII, ignoring non-ASCII characters
    ascii_bytes = decomposed.encode("ascii", "ignore")
    ascii_str = ascii_bytes.decode("ascii")
    # Convert to uppercase
    # Keep only uppercase ASCII letters A-Z
    return re.sub("[^A-Z]", "", ascii_str.upper())


def is_alpha(s: str) -> bool:
    """
    Returns True if all letters are in a-z or A-Z.
    """
    return s.isalpha() and s.isascii()


def check_is_alpha(s: str):
    if not is_alpha(s):
        raise ValueError(f"{s} is not all composed of ascii characters")
