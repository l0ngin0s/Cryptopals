"""
Single-byte XOR cipher
The hex encoded string:

1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736
... has been XOR'd against a single character. Find the key, decrypt the message.

You can do this by hand. But don't: write code to do it for you.

How? Devise some method for "scoring" a piece of English plaintext. Character frequency is a good metric. Evaluate each output and choose the one with the best score.

Achievement Unlocked
You now have our permission to make "ETAOIN SHRDLU" jokes on Twitter.
"""

from Common import en_word_counter, xor_crypter

string = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'.decode('hex')

result = [0, '']

for c in xrange(32, 127):
    m = xor_crypter(c, string, 'IntSrting')
    c = en_word_counter(m)

    if c > result[0]:
        result = [c, m]

print "[!] Target successful: {}".format(result[1])
