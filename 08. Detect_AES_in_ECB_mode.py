"""
Detect AES in ECB mode
In this file (8.txt) are a bunch of hex-encoded ciphertexts.

One of them has been encrypted with ECB.

Detect it.

Remember that the problem with ECB is that it is stateless and deterministic; the same 16 byte plaintext block will always produce the same 16 byte ciphertext.
"""


def is_ecb_detected(chunks):
    for chunk in range(len(chunks)):
        for next_chunk in range(chunk + 1, len(chunks)):
            if chunks[chunk] in chunks[next_chunk]:
                return True
    return False


with open('8.txt', 'r') as f:
    cipher_blocks = f.readlines()

CHUNK_SIZE = 4 * 2
ecb_detected = ''

for c in cipher_blocks:
    blocks = [c[i * CHUNK_SIZE:i * CHUNK_SIZE + CHUNK_SIZE] for i in range(len(c) / CHUNK_SIZE)]
    if is_ecb_detected(blocks):
        ecb_detected = c

print "[!] Target successful: {}".format(ecb_detected)
