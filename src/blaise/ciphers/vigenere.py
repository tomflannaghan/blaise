from .base import Cipher

class Vigenere(Cipher):
    """
    Simple Vigenère cipher implementation.

    The cipher operates on the 26-letter English alphabet.
    Non-alphabetic characters are left unchanged.
    """

    def __init__(self, key: str):
        if not key.isalpha():
            raise ValueError("Key must consist of alphabetic characters only")
        self.key = key.upper()

    def _shift(self, char: str, shift: int) -> str:
        """Shift a single alphabetic character by `shift` positions."""
        if char.isupper():
            base = ord("A")
        else:
            base = ord("a")
        return chr((ord(char) - base + shift) % 26 + base)

    def encrypt(self, data: str) -> str:
        """Encrypt `data` using the Vigenère cipher."""
        result = []
        key_len = len(self.key)
        key_index = 0

        for ch in data:
            if ch.isalpha():
                shift = ord(self.key[key_index % key_len]) - ord("A")
                result.append(self._shift(ch, shift))
                key_index += 1
            else:
                result.append(ch)

        return "".join(result)

    def decrypt(self, data: str) -> str:
        """Decrypt `data` that was encrypted with the Vigenère cipher."""
        result = []
        key_len = len(self.key)
        key_index = 0

        for ch in data:
            if ch.isalpha():
                shift = ord(self.key[key_index % key_len]) - ord("A")
                result.append(self._shift(ch, -shift))
                key_index += 1
            else:
                result.append(ch)

        return "".join(result)


def encrypt_vigenere(plaintext: str, key: str) -> str:
    return Vigenere(key).encrypt(plaintext)


def decrypt_vigenere(ciphertext: str, key: str) -> str:
    return Vigenere(key).decrypt(ciphertext)
