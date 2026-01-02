import importlib.metadata
from blaise.ciphers.vigenere import encrypt_vigenere, decrypt_vigenere

__version__ = importlib.metadata.version(__name__)