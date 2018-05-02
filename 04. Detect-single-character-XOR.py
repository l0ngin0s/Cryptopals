"""
Detect single-character XOR
One of the 60-character strings in this file has been encrypted by single-character XOR.

Find it.

(Your code from #3 should help.)
"""

from Common import en_word_counter, xor_crypter

def decrypt(msg):
    dec = [0, '']

    for c in xrange(32, 127):
        m = xor_crypter(c, msg, 'IntSrting')
        c = en_word_counter(m)

        if c > dec[0]:
            dec = [c, m]
    return dec


f_in = open('4.txt', 'r')
content = f_in.readlines()
f_in.close()

result = [0, '']
for c in content:
    tmp_result = decrypt(c.strip('\n').decode('hex'))
    if tmp_result[0] > result[0]:
        result = tmp_result

print "[!] Target successful: {}".format(result[1])
