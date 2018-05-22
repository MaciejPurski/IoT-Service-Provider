#!/usr/bin/python3.6

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA

class CipherAES:
	def __init__(self):
		self.__key_valid = False
		self.__key = ''

	def set_key(self, new_key_bytes):
		if not isinstance(new_key_bytes, bytes) or len(new_key_bytes) != AES.block_size:
			raise TypeError('Expected 16 bytes buffer')

		self.__key = new_key_bytes
		self.__key_valid = True

	def encrypt_aes(self, buffer):
		if not self.__key_valid:
			raise RuntimeError('Key not initialized')

		iv = Random.new().read(AES.block_size)
		cipher = AES.new(self.__key, AES.MODE_CBC, iv)
		encrypted = iv + cipher.encrypt(CipherAES.pad(buffer))
		print('CryptoCore: Msg length before encryption: {} after: {}'.format(len(buffer), len(encrypted)))

		return encrypted

	def decrypt_aes(self, buffer):
		iv = buffer[:AES.block_size]
		cipher = AES.new(self.__key, AES.MODE_CBC, iv)
		decrypted = CipherAES.unpad(cipher.decrypt(buffer[AES.block_size:]))

		return decrypted

	@staticmethod
	def pad(buf):
		return buf + (AES.block_size - len(buf) % AES.block_size) * chr(AES.block_size - len(buf) % AES.block_size)

	@staticmethod
	def unpad(buf):
		return buf[:-ord(buf[len(buf)-1:])] 

	@staticmethod
	def encrypted_msg_length(length):
		return AES.block_size + length + (AES.block_size - length % AES.block_size)

class CipherRSA:
	def __init__(self, public_key_file, private_key_file):
		self.public_key = RSA.importKey(open(public_key_file).read())
		self.private_key = RSA.importKey(open(private_key_file).read())

		self.priv_cipher = PKCS1_OAEP.new(self.private_key)

		self.signer = PKCS1_v1_5.new(self.private_key)
		self.verifier = PKCS1_v1_5.new(self.public_key)

	def decrypt_rsa(self, buffer):
		return self.priv_cipher.decrypt(buffer)

	def sign(self, msg):
		h = SHA.new(msg)
		return self.signer.sign(h)

	def verify(self, msg, signature):
		h = SHA.new(msg)
		return self.verifier.verify(h, signature)

