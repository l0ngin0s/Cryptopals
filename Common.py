# coding=utf-8
import base64
import sys
from collections import Counter

from Crypto.Cipher import AES
from nltk.corpus import wordnet


def en_word_counter(msg):
    # nltk.download('wordnet')
    s_split = msg.strip('\n').split(' ')
    word_count = 0

    for item in s_split:
        try:
            if wordnet.synsets(item):
                word_count += 1
        except:
            word_count = word_count

    return word_count


def xor_crypter(c1, c2, input_type):
    if input_type == 'HexString':  # HexString: c1 = Hex String, c2 = Hex String
        return ''.join(str(hex(int(x, 16) ^ int(y, 16)).replace('0x', '')) for (x, y) in zip(c1, c2))
    elif input_type == 'IntSrting':  # IntSrting: c1 = int, c2 = String
        return ''.join(chr(c1 ^ ord(x)) for x in c2)
    elif input_type == 'String':
        return ''.join([chr(ord(x) ^ ord(y)) for (x, y) in zip(c1, c2)])


def hamming_distance(s1, s2):
    """
    https://en.wikipedia.org/wiki/Hamming_distance#Algorithm_example
    Return the Hamming distance between equal-length sequences
    """
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")

    s1 = ''.join("{0:08b}".format(ord(c)) for c in s1)
    s2 = ''.join("{0:08b}".format(ord(c)) for c in s2)

    return sum(el1 != el2 for el1, el2 in zip(s1, s2))


def search_key_size(cipher_text=None, max_block_size=None, max_key_size=None):
    """
    Get de KEY SIZE from a rapeating-key XOR cipher.

    + Parameters:
    - cipher_text:      No doubts here ;)
    - max_block_size:   Nº block used to calculate AvgHD (Average Hamming Distance)
    - key_max_size:     Max KEY SIZE to calculate

    Return the KEY SIZE from cipher
    """
    guessing_keys = []

    for blocks in range(2, max_block_size):
        avg = sys.float_info.max
        tmp_guessing_keys = 0

        for key_size in range(2, max_key_size):
            hd = []
            for block in range(1, blocks):
                bk = block * key_size
                # hd.append(float(hamming_distance(cipher_text[bk:bk + 2], cipher_text[bk + 2:bk + 4])) / float(key_size))
                hd.append(float(hamming_distance(cipher_text[bk:bk + 2], cipher_text[bk + 2:bk + 4])))

            # AVG
            tmp_avg = sum(hd) / float(blocks)

            if tmp_avg == avg or tmp_avg < avg:
                avg = tmp_avg
                tmp_guessing_keys = key_size

        guessing_keys.append(tmp_guessing_keys)

    return Counter(guessing_keys).most_common()[0][0]


def get_b64_cipher_file(b64_cipher_file):
    f = open(b64_cipher_file, 'r')
    cipher_text = f.readlines()
    f.close()

    cipher_text = base64.decodestring(''.join(x.strip('\n') for x in cipher_text))

    return cipher_text


def pkcs7_padding(message, block_len):
    padding_len = block_len - len(message) % block_len
    return message + chr(padding_len) * padding_len


def aes_ecb_decipher(cipher_text, key):
    return AES.new(key, AES.MODE_ECB).decrypt(cipher_text)


def cbc_block(vector, block_cipher_decryption):
    return xor_crypter(vector, block_cipher_decryption)


def aes_cbc_decipher(cipher_text, key, iv):
    block_size = 16
    plain_text = ''
    blocks = len(cipher_text) / block_size
    vector = iv

    for b in range(blocks):
        cipher_text_block = cipher_text[b * block_size:b * block_size + block_size]
        block_decipher_decryption = aes_ecb_decipher(cipher_text_block, key)
        plain_text += xor_crypter(vector, block_decipher_decryption, 'String')
        vector = cipher_text_block

    return plain_text


def is_ecb_detected(cipher_text, chunk_size):
    blocks = [cipher_text[i * chunk_size:i * chunk_size + chunk_size] for i in range(len(cipher_text) / chunk_size)]

    for chunk in range(len(blocks)):
        for next_chunk in range(chunk + 1, len(blocks)):
            if blocks[chunk] in blocks[next_chunk]:
                return True
    return False
