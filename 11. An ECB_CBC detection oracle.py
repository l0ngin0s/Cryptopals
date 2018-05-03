"""
An ECB/CBC detection oracle
Now that you have ECB and CBC working:

Write a function to generate a random AES key; that's just 16 random bytes.

Write a function that encrypts data under an unknown key --- that is, a function that generates a random key and encrypts under it.

The function should look like:

encryption_oracle(your-input)
=> [MEANINGLESS JIBBER JABBER]

Under the hood, have the function append 5-10 bytes (count chosen randomly) before the plaintext and 5-10 bytes after the plaintext.

Now, have the function choose to encrypt under ECB 1/2 the time, and under CBC the other half (just use random IVs each time for CBC). Use rand(2) to decide which to use.

Detect the block cipher mode the function is using each time. You should end up with a piece of code that, pointed at a block box that might be encrypting ECB or CBC, tells you which one is happening.
"""

from Crypto.Cipher import AES
from os import urandom
import random

from Common import is_ecb_detected, pkcs7_padding


def append(n):
    return ''.join(chr(c) for c in bytearray(urandom(n)))


def encryption_oracle(plain_text):
    oracle_plain_text = pkcs7_padding(append(random.randint(5, 10)) + plain_text + append(random.randint(5, 10)), 16)

    if random.randint(0, 1) == 0:
        return [AES.new(urandom(16), AES.MODE_CBC, urandom(16)).encrypt(oracle_plain_text), 'CBC']
    else:
        return [AES.new(urandom(16), AES.MODE_ECB).encrypt(oracle_plain_text), 'ECB']


# The 6.dec.txt is the 6.txt file decrypted in challenge 6 --> 'I'm back and I'm ringin' the bell ...'
with open('6.dec.txt', 'r') as f:
    plain_text = f.read()

# 4 bytes chunk
CHUNK_SIZE = 4

for i in range(25):
    a, b = encryption_oracle(plain_text)

    if is_ecb_detected(a, CHUNK_SIZE):
        mode = 'ECB'
    else:
        mode = 'CBC'

    print '[!] Detected {} vs Used {} --> Detection: {}'.format(mode, b, mode == b)
