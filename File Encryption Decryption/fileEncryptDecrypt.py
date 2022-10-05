# This is code for File Encryption Decryption Using AES Algorithms

# Advanced Encryption Standard (AES) is a specification for the encryption of electronic data established by the U.S National Institute of Standards and Technology (NIST) in 2001. AES is widely used today as it is a much stronger than DES and triple DES despite being harder to implement.

# pyAesCrypt is a file encryption module that uses AES256-CBC to encrypt/decrypt files and binary streams. Install pyAesCrypt as follows: pip3 install pyAesCrypt.

# pip install pyAesCrypt

import pyAesCrypt
import sys

def encryptFile(filename, password):    
    pyAesCrypt.encryptFile(filename, filename + ".aes", password)
    print("File Encryption successfully done.")

def decryptFile(filename, password):
    pyAesCrypt.decryptFile(filename + ".aes", filename, password)
    print("File Decryption successfully done.")


# Enter the file in the argument and password also

encryptFile(sys.argv[0], sys.argv[1])
decryptFile(sys.argv[0], sys.argv[1])