import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
import os
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from ast import literal_eval

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode()
unpad = lambda s: s[:-ord(s[len(s)-1:])]

class AESCipher(object):


    def __init__(self, key):
        self.key = hashlib.sha256(AESCipher.str_to_bytes(key)).digest()

    @staticmethod
    def str_to_bytes(data):
        u_type = type(b''.decode('utf8'))
        if isinstance(data, u_type):
            return data.encode('utf8')
        return data


    def encrypt(self, raw):
        raw = pad(AESCipher.str_to_bytes(raw))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode('utf-8')

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')


class RSAPublicKey:
    # private_key = None
    def __init__(self):
        f = open("/etc/letsencrypt/live/api.phopo.best/privkey.pem", 'r')
        self.private_key = RSA.import_key(f.read())

    def decrypt(self, encrypted):
        sentinel = Random.new().read(256)
        decryptor = PKCS1_v1_5.new(self.private_key)
        decrypted = decryptor.decrypt(encrypted,sentinel)
        return decrypted

    def signed_to_unsigned(self, list):
        for count in range(len(list)):
            list[count] = list[count]& 0xFF
        return bytes(list)

    def literal_eval(self, byte_text):
        return literal_eval(byte_text)

    def out_password(self, byte_text):
        print(str(byte_text[0] == '['))
        if byte_text[0] == '[':
            password = self.decrypt(self.signed_to_unsigned(self.literal_eval(byte_text))).decode()
        else:
            password = byte_text
        return password
#-*- coding: utf-8 -*-

# Python 3.4
# author: http://blog.dokenzy.com/
# date: 2015. 4. 8

# import base64
# import hashlib
# from Crypto import Random
# from Crypto.Cipher import AES
#
# # 아마 특정한 블록 사이즈를 채우기 위해서 입력된 값을 임의의 값으로 패딩(채워주기) 하는 코드 인 듯...
# BS = 16
# pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode()
# unpad = lambda s: s[:-ord(s[len(s)-1:])]
#
# # 초기화 코드 인듯
# def iv():
#     """
#     The initialization vector to use for encryption or decryption.
#     It is ignored for MODE_ECB and MODE_CTR.
#     """
#     return chr(0) * 16
#
# # 2교시때 설명했 듯이 클래스는 구조를 잘 잡아주는 껍데기 이다.
# class AESCipher(object):
#     """
#     https://github.com/dlitz/pycrypto
#     """
#
#     def __init__(self, key):
#         self.key = key
#         #self.key = hashlib.sha256(key.encode()).digest()
#
#     # 메시지를 암호화 하는 함수
#     def encrypt(self, message):
#         """
#         It is assumed that you use Python 3.0+
#         , so plaintext's type must be str type(== unicode).
#         """
#         message = message.encode()
#         raw = pad(message)
#         cipher = AES.new(self.key, AES.MODE_CBC, iv())
#         enc = cipher.encrypt(raw)
#         return base64.b64encode(enc).decode('utf-8')
#
#     # 메시지를 복호화 하는 함수
#     def decrypt(self, enc):
#         enc = base64.b64decode(enc)
#         cipher = AES.new(self.key, AES.MODE_CBC, iv())
#         dec = cipher.decrypt(enc)
#         return unpad(dec).decode('utf-8')


# from Crypto.PublicKey import RSA
#
#
# from Crypto import Random
#
# KEY_LENGTH = 2048
# random_generator = Random.new().read
#
# keypair = RSA.generate(KEY_LENGTH, random_generator)
# pubkey = keypair.publickey()
#
# message = "Hello"
#
# encrypt = pubkey.encrypt(message.encode(), 32)
# decrypt = keypair.decrypt(encrypt)
