# Blaise

Blaise is a package for encrypting, decrypting and cracking classical cryptographic ciphers such as Vigenere, Playfair, etc. It's intended for people solving/setting puzzles that utilise classical ciphers.

## Supported Ciphers

- Todo, nothing yet supported!

## Project Structure and Naming

- Each cipher should live in a seperate module in the `ciphers` folder.
- It should provide a `Cipher` subclass named after the name of the cipher, and also utility functions for encrypting and decrypting that should be called `encrypt_XXX` and `decrypt_XXX`.
- If there is a cracking function, it should be called `crack_XXX`.
- The functions should follow standard signatures.

