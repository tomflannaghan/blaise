import pytest
from blaise.ciphers.caesar import Caesar


def test_encrypt_with_positive_shift():
    """Positive key should shift right."""
    plaintext = "HELLO"
    result = Caesar().encrypt(plaintext, key=1)
    assert result == "IFMMP"


def test_encrypt_with_negative_shift():
    """Negative key should shift left."""
    plaintext = "HELLO"
    result = Caesar().encrypt(plaintext, key=-1)
    assert result == "GDKKN"


def test_encrypt_with_zero_shift():
    """Zero key should return plaintext unchanged."""
    plaintext = "HELLO"
    result = Caesar().encrypt(plaintext, key=0)
    assert result == "HELLO"


def test_encrypt_with_wraparound():
    """Shift should wrap around the alphabet."""
    plaintext = "XYZ"
    result = Caesar().encrypt(plaintext, key=3)
    assert result == "ABC"


def test_encrypt_with_full_rotation():
    """Shift by 26 should return plaintext unchanged."""
    plaintext = "HELLO"
    result = Caesar().encrypt(plaintext, key=26)
    assert result == "HELLO"


def test_encrypt_with_key_greater_than_26():
    """Key greater than 26 should be equivalent to key mod 26."""
    plaintext = "HELLO"
    result_27 = Caesar().encrypt(plaintext, key=27)
    result_1 = Caesar().encrypt(plaintext, key=1)
    assert result_27 == result_1


def test_encrypt_empty_string():
    """Encrypting empty string should return empty string."""
    result = Caesar().encrypt("", key=5)
    assert result == ""


def test_decrypt_with_positive_key():
    """Decrypting with positive key should shift left."""
    ciphertext = "IFMMP"
    result = Caesar().decrypt(ciphertext, key=1)
    assert result == "HELLO"


def test_decrypt_with_negative_key():
    """Decrypting with negative key should shift right."""
    ciphertext = "GDKKN"
    result = Caesar().decrypt(ciphertext, key=-1)
    assert result == "HELLO"


def test_decrypt_with_zero_key():
    """Decrypting with zero key should return ciphertext unchanged."""
    ciphertext = "HELLO"
    result = Caesar().decrypt(ciphertext, key=0)
    assert result == "HELLO"


def test_decrypt_with_wraparound():
    """Decryption should wrap around the alphabet."""
    ciphertext = "ABC"
    result = Caesar().decrypt(ciphertext, key=3)
    assert result == "XYZ"


def test_decrypt_empty_string():
    """Decrypting empty string should return empty string."""
    result = Caesar().decrypt("", key=5)
    assert result == ""


def test_encrypt_decrypt_roundtrip():
    """Encryption followed by decryption should return original text."""
    plaintext = "HELLO"
    key = 7
    ciphertext = Caesar().encrypt(plaintext, key=key)
    decrypted = Caesar().decrypt(ciphertext, key=key)
    assert decrypted == plaintext


def test_roundtrip_with_all_keys():
    """Roundtrip should work for all possible keys."""
    plaintext = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
    for key in range(26):
        ciphertext = Caesar().encrypt(plaintext, key=key)
        decrypted = Caesar().decrypt(ciphertext, key=key)
        assert decrypted == plaintext


def test_roundtrip_with_single_character():
    """Roundtrip should work for single characters."""
    for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        key = 13
        ciphertext = Caesar().encrypt(char, key=key)
        decrypted = Caesar().decrypt(ciphertext, key=key)
        assert decrypted == char


def test_crack():
    plaintext = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
    ciphertext = Caesar().encrypt(plaintext, 23)
    assert ciphertext == "QEBNRFZHYOLTKCLUGRJMPLSBOQEBIXWVALD"
    result = Caesar().crack(ciphertext)
    assert len(result) == 26
    assert result[0].to_dicts()[0] == pytest.approx(
        {
            "key": 23,
            "plaintext": plaintext,
            "score": 1.1898997492680905,
        }
    )
