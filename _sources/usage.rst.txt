Usage
=====

The :mod:`blaise` package provides a simple API for encryption.

.. code-block:: python

    from blaise import encrypt_vigenere

    ciphertext = encrypt_vigenere("HELLO", "KEY")
