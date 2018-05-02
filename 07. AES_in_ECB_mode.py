"""
AES in ECB mode
The Base64-encoded content in this file has been encrypted via AES-128 in ECB mode under the key

"YELLOW SUBMARINE".
(case-sensitive, without the quotes; exactly 16 characters; I like "YELLOW SUBMARINE" because it's exactly 16 bytes long, and now you do too).

Decrypt it. You know the key, after all.

Easiest way: use OpenSSL::Cipher and give it AES-128-ECB as the cipher.

Do this with code.
You can obviously decrypt this using the OpenSSL command-line tool, but we're having you get ECB working in code for a reason. You'll need it a lot later on, and not just for attacking ECB.
"""

from Crypto.Cipher import AES
from Common import get_b64_cipher_file

# 1. Getting cipher
cipher_text = get_b64_cipher_file('7.txt')

# 2. Decrypt cipher text
decipher_text = AES.new("YELLOW SUBMARINE", AES.MODE_ECB).decrypt(cipher_text)

# 3. Last, create a decipher text file
f = open('7.dec.txt', 'w')
f.write(decipher_text)
f.close()

print "[!] Target successful: {}".format('')
