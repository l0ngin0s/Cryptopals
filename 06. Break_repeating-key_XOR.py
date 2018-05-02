"""
Break repeating-key XOR
It is officially on, now.
This challenge isn't conceptually hard, but it involves actual error-prone coding. The other challenges in this set are there to bring you up to speed. This one is there to qualify you. If you can do this one, you're probably just fine up to Set 6.

There's a file here. It's been base64'd after being encrypted with repeating-key XOR.

Decrypt it.

Here's how:

Let KEYSIZE be the guessed length of the key; try values from 2 to (say) 40.
Write a function to compute the edit distance/Hamming distance between two strings. The Hamming distance is just the number of differing bits. The distance between:
this is a test
and
wokka wokka!!!
is 37. Make sure your code agrees before you proceed.
For each KEYSIZE, take the first KEYSIZE worth of bytes, and the second KEYSIZE worth of bytes, and find the edit distance between them. Normalize this result by dividing by KEYSIZE.
The KEYSIZE with the smallest normalized edit distance is probably the key. You could proceed perhaps with the smallest 2-3 KEYSIZE values. Or take 4 KEYSIZE blocks instead of 2 and average the distances.
Now that you probably know the KEYSIZE: break the ciphertext into blocks of KEYSIZE length.
Now transpose the blocks: make a block that is the first byte of every block, and a block that is the second byte of every block, and so on.
Solve each block as if it was single-character XOR. You already have code to do this.
For each block, the single-byte XOR key that produces the best looking histogram is the repeating-key XOR key byte for that block. Put them together and you have the key.
This code is going to turn out to be surprisingly useful later on. Breaking repeating-key XOR ("Vigenere") statistically is obviously an academic exercise, a "Crypto 101" thing. But more people "know how" to break it than can actually break it, and a similar technique breaks something much more important.

No, that's not a mistake.
We get more tech support questions for this challenge than any of the other ones. We promise, there aren't any blatant errors in this text. In particular: the "wokka wokka!!!" edit distance really is 37.
"""

from collections import Counter
from Common import search_key_size, xor_crypter, get_b64_cipher_file

# 1. Get the cipher file
cipher_text = get_b64_cipher_file('6.txt')

# 3. Calculating Key Size
key_size = search_key_size(cipher_text, 10, 40)

# Next code is from http://perso.heavyberry.com/articles/2015-01/cryptopals --------------------------------------------
# It's amazing how axiomiety has solved it!

# 4. Transposing and break the ciphertext into blocks of KEYSIZE length
transposed_list = [cipher_text[i::key_size] for i in range(key_size)]

# 5. For each block, the single-byte XOR key that produces the best looking histogram is the repeating-key XOR key byte
# for that block.
#
# Computer QWERTY Keyboard Key Frequency (http://letterfrequency.org/)
most_common_computer_qwerty_char = ord(' ')
xor_key = bytearray()
for block in transposed_list:
    c = Counter(block)  # from collections import Counter
    most_common_char_in_block, value = c.most_common()[0]
    xor_key.append(ord(most_common_char_in_block) ^ most_common_computer_qwerty_char)
# ----------------------------------------------------------------------------------------------------------------------

# 6. Last, create a decipher text file
key = '{}{}'.format(xor_key * (len(cipher_text) / len(xor_key)), xor_key[:len(cipher_text) % len(xor_key)])
decipher_text = xor_crypter(key, cipher_text, 'String')

f = open('6.dec.txt', 'w')
f.write(decipher_text)
f.close()

print "[!] Target successful: {}".format(xor_key)
