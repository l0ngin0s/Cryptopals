"""
Detect AES in ECB mode
In this file (8.txt) are a bunch of hex-encoded ciphertexts.

One of them has been encrypted with ECB.

Detect it.

Remember that the problem with ECB is that it is stateless and deterministic; the same 16 byte plaintext block will always produce the same 16 byte ciphertext.
"""
from Common import is_ecb_detected

with open('8.txt', 'r') as f:
    cipher_blocks = f.readlines()

CHUNK_SIZE = 4 * 2
ecb_detected = ''

for c in cipher_blocks:
    if is_ecb_detected(c, CHUNK_SIZE):
        ecb_detected = c

print "[!] Target successful: {}".format(ecb_detected)
