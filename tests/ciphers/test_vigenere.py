import pytest

from blaise.ciphers.vigenere import encrypt_vigenere, decrypt_vigenere


def test_encrypt_decrypt_roundtrip():
    """Encryption followed by decryption should return the original text."""
    plaintext = "HELLO WORLD! 123"
    ciphertext = encrypt_vigenere(plaintext, "KEY")
    assert ciphertext != plaintext  # should be different
    assert decrypt_vigenere(ciphertext, "KEY") == plaintext


def test_non_alpha_characters_unchanged():
    """Non‑alphabetic characters should be preserved unchanged."""
    plaintext = "123-!@#"
    assert encrypt_vigenere(plaintext, "ABC") == plaintext
    assert decrypt_vigenere(plaintext, "ABC") == plaintext


def test_key_case_insensitivity_and_uppercase_output():
    """Key should be case‑insensitive and output should preserve case of plaintext."""
    plaintext = "AbC"
    ciphertext = encrypt_vigenere(plaintext, "kEy")
    # The key is treated as "KEY", so shifts are 10, 4, 24
    assert ciphertext == "KfA"
    assert decrypt_vigenere(ciphertext, "kEy") == plaintext


def test_invalid_key_raises():
    """Providing a non‑alphabetic key should raise ValueError."""
    with pytest.raises(ValueError):
        encrypt_vigenere("foo", "KEY123")
    with pytest.raises(ValueError):
        encrypt_vigenere("foo", "")


def test_encrypt_decrypt_consistency_with_known_values():
    """Known Vigenère cipher example from Wikipedia."""
    plaintext = "ATTACKATDAWN"
    expected_ciphertext = "LXFOPVEFRNHR"
    assert encrypt_vigenere(plaintext, "LEMON") == expected_ciphertext
    assert decrypt_vigenere(expected_ciphertext, "LEMON") == plaintext
