from cryptography.fernet import Fernet

''' generate_key() method generates a new fernet key. The key must be kept safe as it is the most important component to decrypt the ciphertext. '''

key = Fernet.generate_key()

file = open("encryption_key.txt", 'wb')

file.write(key)

file.close()