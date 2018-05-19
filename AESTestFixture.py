#!/usr/bin/python3.6

import unittest

from Crypto import Random
from CryptoCore import CipherAES
from Crypto.Cipher import AES
import random

class AESTestCase(unittest.TestCase):
	def setUp(self):
		key = Random.new().read(AES.block_size) 
		self.cipher = CipherAES()
		self.cipher.set_key(key)
		

	def test_short_msg(self):
		msg = 'abcdef'
		encrypted = self.cipher.encrypt_aes(msg)
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