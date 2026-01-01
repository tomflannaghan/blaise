import pytest

from blaise.ciphers.vigenere import Vigenere


def test_encrypt_decrypt_roundtrip():
    """Encryption followed by decryption should return the original text."""
    cipher = Vigenere("KEY")
    plaintext = "HELLO WORLD! 123"
    ciphertext = cipher.encrypt(plaintext)
    assert ciphertext != plaintext  # should be different
    assert cipher.decrypt(ciphertext) == plaintext


def test_non_alpha_characters_unchanged():
    """Non‑alphabetic characters should be preserved unchanged."""
    cipher = Vigenere("ABC")
    plaintext = "123-!@#"
    assert cipher.encrypt(plaintext) == plaintext
    assert cipher.decrypt(plaintext) == plaintext


def test_key_case_insensitivity_and_uppercase_output():
    """Key should be case‑insensitive and output should preserve case of plaintext."""
    cipher = Vigenere("kEy")
    plaintext = "AbC"
    ciphertext = cipher.encrypt(plaintext)
    # The key is treated as "KEY", so shifts are 10, 4, 24
    assert ciphertext == "KfA"
    assert cipher.decrypt(ciphertext) == plaintext


def test_invalid_key_raises():
    """Providing a non‑alphabetic key should raise ValueError."""
    with pytest.raises(ValueError):
        Vigenere("KEY123")
    with pytest.raises(ValueError):
        Vigenere("")


def test_encrypt_decrypt_consistency_with_known_values():
    """Known Vigenère cipher example from Wikipedia."""
    cipher = Vigenere("LEMON")
    plaintext = "ATTACKATDAWN"
    expected_ciphertext = "LXFOPVEFRNHR"
    assert cipher.encrypt(plaintext) == expected_ciphertext
    assert cipher.decrypt(expected_ciphertext) == plaintext