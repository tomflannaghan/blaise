import pytest

from blaise.ciphers.vigenere import vigenere_crack, vigenere_encrypt, vigenere_decrypt


def test_encrypt_decrypt_roundtrip():
    """Encryption followed by decryption should return the original text."""
    plaintext = "HELLOWORLD"
    ciphertext = vigenere_encrypt(plaintext, "KEY")
    assert ciphertext != plaintext  # should be different
    assert vigenere_decrypt(ciphertext, "KEY") == plaintext


def test_non_alpha_characters_stripped():
    """Non‑alphabetic characters should be stripped."""
    assert vigenere_encrypt("123-!@#", "ABC") == ""
    assert vigenere_decrypt("123-!@#", "ABC") == ""


def test_key_case_insensitivity_and_uppercase_output():
    """Key should be case-insensitive and output should be upper case."""
    plaintext = "AbC"
    ciphertext = vigenere_encrypt(plaintext, "kEy")
    # The key is treated as "KEY", so shifts are 10, 4, 24
    assert ciphertext == "KFA"
    assert vigenere_decrypt(ciphertext, "kEy") == plaintext.upper()


def test_invalid_key_raises():
    """Providing a non‑alphabetic key should raise ValueError."""
    with pytest.raises(ValueError):
        vigenere_encrypt("foo", "KEY123")
    with pytest.raises(ValueError):
        vigenere_encrypt("foo", "")


def test_encrypt_decrypt_consistency_with_known_values():
    """Known Vigenère cipher example from Wikipedia."""
    plaintext = "ATTACKATDAWN"
    expected_ciphertext = "LXFOPVEFRNHR"
    assert vigenere_encrypt(plaintext, "LEMON") == expected_ciphertext
    assert vigenere_decrypt(expected_ciphertext, "LEMON") == plaintext


def test_vigenere_crack():
    plaintext = "THEVIGENERECIPHERISUSEDTOENCODEPLAINTEXTINTOCIPHERTEXT"
    key = "ARSE"
    ciphertext = vigenere_encrypt(plaintext, key)
    results = vigenere_crack(ciphertext, key_length=[3, 4, 5], n_trials=100, top_n=10)
    assert results[0].to_dicts()[0] == {
        "key": "ARSE",
        "plaintext": plaintext,
        "score": 0.7612071669180257,
    }
    assert len(results) == 10
