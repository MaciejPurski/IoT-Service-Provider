#!/usr/bin/python3.6

import unittest

from Crypto import Random
from CryptoCore import CipherAES
from Crypto.Cipher import AES
import random

class AESTestCase(unittest.TestCase):
	def setUp(self):
		key_file = open('key', 'wb')
		key = Random.new().read(AES.block_size)
		key = b'DUPADUPADUPADUPA'
		key_file.write(key)
		key_file.close()
		self.cipher = CipherAES()
		self.cipher.set_key(key)

	def test_short_msg(self):
		msg = b'abcdef'
		in_file = open('in', 'wb')
		in_file.write(msg)
		in_file.close()

		encrypted = self.cipher.encrypt_aes(msg)
		encr_file = open('encrypted', 'wb')
		encr_file.write(encrypted)
		encr_file.close()
		decrypted = self.cipher.decrypt_aes(encrypted)

		self.assertEqual(msg, decrypted)
		self.assertEqual(len(encrypted), AES.block_size + len(CipherAES.pad(msg)))


	def test_random_long_msgs(self):
		random.seed()
		for i in range(0, 100):
			length = random.randint(32, 1024)
			msg = Random.new().read(length)

			encrypted = self.cipher.encrypt_aes(msg)
			decrypted = self.cipher.decrypt_aes(encrypted)

			self.assertEqual(msg, decrypted)
			self.assertEqual(len(encrypted), AES.block_size + len(CipherAES.pad(msg)))


if __name__ == '__main__':
    unittest.main()