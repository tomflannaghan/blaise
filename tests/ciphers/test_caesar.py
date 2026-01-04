from blaise.ciphers.caesar import caesar_crack, caesar_encrypt, caesar_decrypt


def test_encrypt_with_positive_shift():
    """Positive key should shift right."""
    plaintext = "HELLO"
    result = caesar_encrypt(plaintext, key=1, is_norm=True)
    assert result == "IFMMP"


def test_encrypt_with_negative_shift():
    """Negative key should shift left."""
    plaintext = "HELLO"
    result = caesar_encrypt(plaintext, key=-1, is_norm=True)
    assert result == "GDKKN"


def test_encrypt_with_zero_shift():
    """Zero key should return plaintext unchanged."""
    plaintext = "HELLO"
    result = caesar_encrypt(plaintext, key=0, is_norm=True)
    assert result == "HELLO"


def test_encrypt_with_wraparound():
    """Shift should wrap around the alphabet."""
    plaintext = "XYZ"
    result = caesar_encrypt(plaintext, key=3, is_norm=True)
    assert result == "ABC"


def test_encrypt_with_full_rotation():
    """Shift by 26 should return plaintext unchanged."""
    plaintext = "HELLO"
    result = caesar_encrypt(plaintext, key=26, is_norm=True)
    assert result == "HELLO"


def test_encrypt_with_key_greater_than_26():
    """Key greater than 26 should be equivalent to key mod 26."""
    plaintext = "HELLO"
    result_27 = caesar_encrypt(plaintext, key=27, is_norm=True)
    result_1 = caesar_encrypt(plaintext, key=1, is_norm=True)
    assert result_27 == result_1


def test_encrypt_empty_string():
    """Encrypting empty string should return empty string."""
    result = caesar_encrypt("", key=5, is_norm=True)
    assert result == ""


def test_decrypt_with_positive_key():
    """Decrypting with positive key should shift left."""
    ciphertext = "IFMMP"
    result = caesar_decrypt(ciphertext, key=1, is_norm=True)
    assert result == "HELLO"


def test_decrypt_with_negative_key():
    """Decrypting with negative key should shift right."""
    ciphertext = "GDKKN"
    result = caesar_decrypt(ciphertext, key=-1, is_norm=True)
    assert result == "HELLO"


def test_decrypt_with_zero_key():
    """Decrypting with zero key should return ciphertext unchanged."""
    ciphertext = "HELLO"
    result = caesar_decrypt(ciphertext, key=0, is_norm=True)
    assert result == "HELLO"


def test_decrypt_with_wraparound():
    """Decryption should wrap around the alphabet."""
    ciphertext = "ABC"
    result = caesar_decrypt(ciphertext, key=3, is_norm=True)
    assert result == "XYZ"


def test_decrypt_empty_string():
    """Decrypting empty string should return empty string."""
    result = caesar_decrypt("", key=5, is_norm=True)
    assert result == ""


def test_encrypt_decrypt_roundtrip():
    """Encryption followed by decryption should return original text."""
    plaintext = "HELLO"
    key = 7
    ciphertext = caesar_encrypt(plaintext, key=key, is_norm=True)
    decrypted = caesar_decrypt(ciphertext, key=key, is_norm=True)
    assert decrypted == plaintext


def test_roundtrip_with_all_keys():
    """Roundtrip should work for all possible keys."""
    plaintext = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
    for key in range(26):
        ciphertext = caesar_encrypt(plaintext, key=key, is_norm=True)
        decrypted = caesar_decrypt(ciphertext, key=key, is_norm=True)
        assert decrypted == plaintext


def test_roundtrip_with_single_character():
    """Roundtrip should work for single characters."""
    for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        key = 13
        ciphertext = caesar_encrypt(char, key=key, is_norm=True)
        decrypted = caesar_decrypt(ciphertext, key=key, is_norm=True)
        assert decrypted == char


def test_crack():
    plaintext = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
    ciphertext = caesar_encrypt(plaintext, 23, is_norm=True)
    assert ciphertext == "QEBNRFZHYOLTKCLUGRJMPLSBOQEBIXWVALD"
    result = caesar_crack(ciphertext)
    assert len(result) == 26
    assert result[0] == (23, plaintext)
