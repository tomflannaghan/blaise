
from abc import abstractmethod


class Cipher:
    """
    The Cipher base class. It can encrpyt/decrypt data with no additional information, so all
    information required to do those tasks should be passed into the init function.
    """

    @abstractmethod
    def decrypt(self, data: str) -> str:
        pass

    @abstractmethod
    def encrypt(self, data: str) -> str:
        pass