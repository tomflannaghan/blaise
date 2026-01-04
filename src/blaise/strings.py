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
    # If already normalized, we are done.
    if is_alpha(s):
        return s.upper()
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


def restore_string(input_string, result_string):
    """
    Restores the non-letter characters present in the input string into the result string.
    The strings must have the same number of letters and the result string must already
    be normalized. Note, does not restore the case of the input string.
    """
    norm_input = normalize_string(input_string)
    if len(norm_input) != len(result_string):
        raise ValueError(
            f"{input_string} and {result_string} have different number of letters"
        )
    # Build the restored string by walking the original string
    result_iter = iter(result_string)
    restored: list[str] = []
    for ch in input_string:
        if is_alpha(ch):
            try:
                restored.append(next(result_iter))
            except StopIteration:
                raise ValueError("More letters in input than in result_string")
        else:
            restored.append(ch)
    # Ensure all letters from result_string were used
    try:
        next(result_iter)
        raise ValueError("More letters in result_string than in input")
    except StopIteration:
        pass
    return "".join(restored)
